import utils
import asyncio
import aiohttp

class Danbooru:
    def __init__(self, file:str):
        utils.make_inner_img_dir('Danbooru')
        self.base_url = 'https://danbooru.donmai.us/posts'
        self.imgs:list[str] = utils.get_img_ids(file)
        self.loc = './img/Danbooru/'
        self.file = './details/danbooru.json'
        asyncio.run(self.run())

    async def get_data(self,img_id:str, session):
        '''
        Gets data (tags and image) from image id and saves it.
        '''
        url = f"{self.base_url}/{img_id}"
        url_j = url+".json"
        details = {}
        async with session.get(url_j) as resp:
            if resp.status != 200:
                print(f'Error:{resp.status} occured when gathering site data for {img_id}.')
                return
            details = await resp.json()
        asyncio.create_task(self.get_tags(img_id,details))
        url_img = details['file_url']
        file_name = f"{img_id}.{details['file_ext']}"
        async with session.get(url_img) as img_resp:
            if img_resp.status != 200:
                print(f'Error:{img_resp.status} occured when gathering img data for {img_id}.')
                return
            with open(f'{self.loc}{file_name}','wb') as img_file:
                async for chunk in img_resp.content.iter_chunked(16):
                    img_file.write(chunk)
                print(f'Image {file_name} downloaded..')

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            load_file = utils.json_read(self.file)
            for img in self.imgs:
                if img == '\n' or img == '\t' or img == '':
                    continue
                if img in load_file.keys():
                    print(f'{img} already has tags in the file.')
                    continue
                tasks.append(asyncio.ensure_future(self.get_data(img, session)))
            temp = await asyncio.gather(*tasks)
            print('\nWork is finished!!!')
        
    async def get_tags(self,img_id:str, data:dict):
        '''
        Gets tags and dumps it in files.
        '''
        character = data['tag_string_character']
        origin = data['tag_string_copyright']
        artist = data["tag_string_artist"]

        tags = data['tag_string_general']
        spaced_tags = tags.replace(" ", ", ")

        json_data = utils.json_read(self.file)

        curr_details:dict ={
                            "character":character,
                            "origin":origin,
                            "artist":artist,
                            "tags":spaced_tags
                        }    
        json_data[img_id] = curr_details
        utils.json_dump(json_data, self.file)
