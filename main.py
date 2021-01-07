from reddit import *
from insta import *
from config import config
import os
import random
import time

subreddit = config['sub_reddit']


if not os.path.exists(f'images/named/{subreddit}'):
    os.makedirs(f'images/named/{subreddit}')

if os.path.exists('images/temp'):
    flist=os.listdir('images/temp')
    for f in flist:
        os.remove(f'images/temp/{f}')

def caption_extraction(file):
    text = file.replace('.png','').replace('.jpg','').replace('.jpeg','')
    caption = config['before_caption']+text.replace('_',' ')+config['after_caption']
    return caption




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
            insta_upload(f'images/Temp/{file}',caption_extraction(file))
            os.rename(f'images/Temp/{file}.REMOVE_ME',f'images/temp/{file}')
            print('uploaded',file)
            os.rename(f'images/Temp/{file}','images/used/uploaded/'+file)
            test=False
        except:
            print('error')
            os.rename(f'images/temp/{file}','images/used/error/'+file)
    time.sleep(config['often'])
