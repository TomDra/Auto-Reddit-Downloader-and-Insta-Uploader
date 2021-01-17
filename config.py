
config = {
    #REDDIT:
    'client_id':'REDDIT_CLIENT_ID', #Get these at www.reddit.com/prefs/apps
    'client_secret':'REDDIT_CLIENT_SECRET',
    'sub_reddit':'SUBREDDIT',           #The subreddit to scrape
    'images':100,                   #number of images per search
    'order':'hot',                  #new/top/hot
    'nsfw':False,                   #Is the subreddit nsfw? True/False
    'del':True,                     #delete duplicate files? True/False (Keep true if not sure)
    #INSTAGRAM:
    'insta_username':'INSTAGRAM_USERNAME',
    'insta_password':'INSTAGRAM_PASSWORD',
    'often':32400,                  #How often should a photo be uploaded (seconds)
    'before_caption':'',            #before and after caption (Good for hastags)
    'after_caption':'#memes',
    #PHOTO:
    'filter':False,                  #Filter images based on text in the photo? (If False ignore beneath)
    'tess_path':r'C:\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',  #Download it here - https://github.com/tesseract-ocr/tesseract
    'words':'Reddit Upvote r/'         #Filter images that include (Seperate words by spaces)
    
    }

