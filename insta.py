def insta_upload(file, caption):
        from instabot import Bot
        from config import config
        insta=Bot()
        insta.login(username = config['insta_username'],
                    password = config['insta_password'])
        insta.upload_photo(file,caption)
