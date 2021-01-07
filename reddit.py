import os
import re
import requests
import praw
import configparser
import concurrent.futures
import argparse
import shutil
from config import config


class redditImageScraper:
    def __init__(self, sub, limit, order, nsfw):
        self.sub = sub
        self.limit = limit
        self.order = order
        self.nsfw = nsfw
        self.name = ''
        self.path = f'images/downloaded/{self.sub}/'
        self.reddit = praw.Reddit(client_id=config['client_id'],
                                  client_secret=config['client_secret'],
                                  user_agent='Reddit Image Downloader')

    def captions(self, image):
        file_name = (image['url'].replace('https://i.redd.it/',''))#.replace('\n','')
        temp = ((file_name.replace('.jpg','')).replace('.png','')).replace('jpeg','')
        extension = file_name.replace(temp,'')
        space_to_under = image['name'].replace(' ','_')
        if space_to_under+extension in os.listdir(f'images/named/{self.sub}') or space_to_under+extension in os.listdir('images/used/uploaded') or space_to_under+extension in os.listdir('images/used/error'):
            shutil.move(self.path+file_name,'images/temp/'+file_name)
        else: shutil.move(self.path+file_name, f'images/named/{self.sub}/'+space_to_under+extension)

    def download(self, image):
        r = requests.get(image['url'])
        with open(image['fname'], 'wb') as f:
            f.write(r.content)
            self.captions(image)

    def start(self):
        images = []
        try:
            go = 0
            if self.order == 'hot':
                submissions = self.reddit.subreddit(self.sub).hot(limit=None)
            elif self.order == 'top':
                submissions = self.reddit.subreddit(self.sub).top(limit=None)
            elif self.order == 'new':
                submissions = self.reddit.subreddit(self.sub).new(limit=None)
            for submission in submissions:
                self.name = submission.title
                if not submission.stickied and submission.over_18 == self.nsfw \
                    and submission.url.endswith(('jpg', 'jpeg', 'png')):
                    fname = self.path + re.search('(?s:.*)\w/(.*)', submission.url).group(1)
                    if not os.path.isfile(fname):
                        images.append({'url': submission.url, 'fname': fname,  'name':submission.title})
                        go += 1
                        if go >= self.limit:
                            break
            if len(images):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                if not os.path.exists(f'images/named/{self.sub}/'):
                    os.makedirs(f'images/named/{self.sub}/')
                if not os.path.exists('images/temp/'):
                    os.makedirs('images/temp/')
                if not os.path.exists('images/used/error/'):
                    os.makedirs('images/used/error/')
                if not os.path.exists('images/used/uploaded'):
                    os.makedirs('images/used/uploaded')
                with concurrent.futures.ThreadPoolExecutor() as ptolemy:
                    ptolemy.map(self.download, images)
        except Exception as e:
            print(e)

def reddit_scrape():
    subreddit = config['sub_reddit']
    images = config['images']
    order = config['order']
    nsfw = config['nsfw']
    scraper = redditImageScraper(subreddit, int(images), order, nsfw)
    scraper.start()
    if config['del']==True:
        shutil.rmtree(f'images/downloaded/{subreddit}')


if __name__ == '__main__':
    reddit_scrape()
