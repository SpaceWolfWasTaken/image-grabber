import json
import os

def json_read(file:str) -> dict:
    '''
    Reads a json file and returns a dict. If it cannot load file, it returns an empty dict.
    If the file doesn't exist, it makes the file and returns an empty dict.
    '''
    try:
        with open(file) as jsonfile: 
            try:
                return json.load(jsonfile)
            except:
                return dict()
    except:
        with open(file, 'w', encoding='utf-8') as make_file:
            make_file.write('')    
        return dict()
    
def make_outer_img_dir():
    '''
    Makess img and details folder if they don't exist.
    '''
    if not os.path.exists(f'img'):
        os.mkdir(f'img')
    if not os.path.exists(f'details'):
        os.mkdir(f'details')
def make_inner_img_dir(name:str):
    '''
    Makes folder name if it doesn't exist in img folder.
    '''
    if not os.path.exists(f'img/{name}'):
        os.mkdir(f'img/{name}')

def json_buffer(buffer):
    '''
    converts a json-like string or bytearray to dictionary
    '''
    return json.loads(buffer)

def json_dump(data:dict, file:str):
    '''Dumps json data into a json file'''
    with open(file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data,jsonfile, indent=4,ensure_ascii=False)

def get_img_ids(file:str) -> list[str]:
    '''
    Opens file and returns a list of image IDs.
    '''
    with open(file) as fl:
        imgs = fl.readlines()
        for i in range(len(imgs)):
            imgs[i] = imgs[i].replace('\n','').strip()
        return imgs

