import asyncio
import aiohttp
from bs4 import BeautifulSoup
import utils

class Pixiv:
    def __init__(self, file:str):
        utils.make_inner_img_dir('Pixiv')
        self.base_url = 'https://www.pixiv.net/en/artworks'
        self.referer = "https://www.pixiv.net/" #works
        self.imgs = utils.get_img_ids(file)
        self.loc = './img/Pixiv/'
        self.file = './details/pixiv.json'
        asyncio.run(self.run())

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            load_file = utils.json_read(self.file)
            for img in self.imgs:
                if img == '\n' or img == '\t' or img == '':
                    continue
                if img in load_file.keys():
                    print(f'{img} data already exists in the file.')
                    continue
                tasks.append(asyncio.ensure_future(self.get_data(img, session)))
            temp = await asyncio.gather(*tasks)
            print('\nWork is finished!!!')
            
    async def get_data(self, img_id:str, session):
        json_data = utils.json_read(self.file)
        for key in json_data:
            if key == img_id:
                print(f"{img_id} already exists.\n")
                return
        orig_url = f'{self.base_url}/{img_id}'
        async with session.get(orig_url,headers = {'accept-language':'en-US'}) as data_resp:
            if data_resp.status != 200:
                print(f"Error:{data_resp.status}")
                return
            soup = BeautifulSoup(await data_resp.read(), 'html.parser')
            meta = soup.find(id='meta-preload-data')
            data = utils.json_buffer(meta['content'])
            self.get_info(img_id,data)
            img_time = data['illust'][img_id]["userIllusts"][img_id]['createDate']
            no_of_imgs = data['illust'][img_id]["pageCount"]
            urls = self.parse_link(img_id,img_time, no_of_imgs)
            imgs_tasks = []
            for i in range(len(urls)):
                imgs_tasks.append(asyncio.ensure_future(self.download_img(urls[i],session,img_id,i)))
            await asyncio.gather(*imgs_tasks)

    async def download_img(self,url,session, img_id, img_no):
        '''
        Downloads the image.
        '''
        print(f'Downloading {img_id}_{img_no}')
        async with session.get(url,headers = {'referer': self.referer}) as resp:
            if resp.status != 200:
                print(f"Error:{resp.status}")
                return
            loc = f'{self.loc}{img_id}_{img_no}.jpg'
            with open(loc, 'wb') as file:
                async for chunk in resp.content.iter_chunked(16):
                    file.write(chunk)
            print(f'Image: {img_id}_{img_no} downloaded!')
        
    def parse_link(self,id, date_time:str, no_of_imgs:int):
        '''
        Generates the link of actual image stored in the server.
        '''
        urls = []
        divided_dt = date_time.split('T')
        date = divided_dt[0].split('-')
        time_and_zone = divided_dt[1].split('+')
        time = time_and_zone[0].split(':')
        for i in range(no_of_imgs):
            url = f"https://i.pximg.net/img-original/img/{date[0]}/{date[1]}/{date[2]}/{time[0]}/{time[1]}/{time[2]}/{id}_p{i}.jpg"
            urls.append(url)
        return urls
    
    def get_info(self, img_id:str, data:dict):
        '''
        Gets data about image, specifically tags, author, authorId, and no. of images.
        '''
        tags = data["illust"][img_id]["tags"]["tags"][0]
        author = tags["userName"]
        author_id = data["illust"][img_id]["tags"]["authorId"]
        no_of_imgs = data['illust'][img_id]["pageCount"]
        link = self.base_url+"/"+img_id
        json_data = utils.json_read(self.file)
        json_data[img_id] = {"author":author,"author-id":author_id,"image-count":no_of_imgs,"source":link}
        utils.json_dump(json_data,self.file)
                    
