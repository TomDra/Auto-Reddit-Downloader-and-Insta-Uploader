from reddit import *
from insta import *
from config import config
import os
import random
import time
from PIL import Image
import pytesseract
subreddit = config['sub_reddit']


if os.path.exists('images/temp'):
    flist=os.listdir('images/temp')
    for f in flist:
        os.remove(f'images/temp/{f}')
if not os.path.exists(f'images/named/{subreddit}/'):
                    os.makedirs(f'images/named/{subreddit}/')
                    
def caption_extraction(file):
    text = file.replace('.png','').replace('.jpg','').replace('.jpeg','')
    caption = config['before_caption']+text.replace('_',' ')+config['after_caption']
    return caption
def photo_filter(file, string):
    pytesseract.pytesseract.tesseract_cmd = config['tess_path']
    filter_words = string.split(' ')
    photo_text = pytesseract.image_to_string(Image.open(f'images/temp/{file}'), lang = 'eng')
    for filter_word in filter_words:
        if filter_word.lower() in photo_text.lower():
            print(f'Filtered {file} because it contained - {filter_word}')
            return True
    return False
        
def upload_and_move(subreddit,file):
    insta_upload(f'images/Temp/{file}',caption_extraction(file))
    os.rename(f'images/Temp/{file}.REMOVE_ME',f'images/temp/{file}')
    print('uploaded',file)
    os.rename(f'images/Temp/{file}','images/used/uploaded/'+file)

active=True
while active == True:
    if len(os.listdir(f'images/named/{subreddit}')) <= config['images']:
        reddit_scrape()
        print('Collected More Photos')
    test=True
    while test==True:
        try:
            files = os.listdir('images/named/'+subreddit)
            file = random.choice(files)
            os.rename(f'images/named/{subreddit}/{file}','images/temp/'+file)
            if config['filter']:
                if photo_filter(file, config['words']):
                    os.rename(f'images/temp/{file}',f'images/used/filtered/{file}')
                    print(f'Filtered out {file}')
                else:
                    upload_and_move(subreddit,file)
                    test=False
            else:
                upload_and_move(subreddit,file)
                test=False
        except Exception as error:
            print('error',error)
            os.rename(f'images/temp/{file}','images/used/error/'+file)
    time.sleep(config['often'])
