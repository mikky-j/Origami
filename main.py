#! usr/env/python3
import os
import re
import praw
from decouple import config
import requests
import shutil


class Origami:
    def __init__(self):
        self.CLIENT_ID = config('CLIENT_ID')
        self.CLIENT_SECRET = config('CLIENT_SECRET')
        self.USER_AGENT = config('USER_AGENT')
        self.USERNAME = config('USERNAME')
        self.PASSWORD = config('PASSWORD')
        self.REDIRECT_URI = "http://localhost:8080"
        self.CODE = config('CODE')
        self.REFRESH_TOKEN = config("REFRESH_TOKEN")
        self.wallpaper_folder = "/home/dami/Downloads/wallpapers/"

    def initialize_reddit_client(self):
        reddit_authorized = praw.Reddit(
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            redirect_uri=self.REDIRECT_URI,
            user_agent=self.USER_AGENT,
        )
        return reddit_authorized

    def move_to_a_save_folder(self, old, new):
        shutil.move(old, new)
        return True

    def download_file(self, title, link: str):
        image = requests.get(
            # This just strips out somethings
            link[11:len(link)-1],
            allow_redirects=True
        )

        # Check if it is a 200 code that the requests stores
        if image.status_code < 300:
            print("writing to the file")

            # Writing to the file using "wb" so that I can write the bits to the image
            with open(title + ".jpg", 'wb') as file:
                file.write(image.content)
                file.close()

            filename = title+".jpg"

            if os.path.exists(filename):
                self.move_to_a_save_folder(
                    filename, self.wallpaper_folder+filename)

        else:
            # Works if somthing goes wrong
            return False
            print("Something went wrong somewhere")
        return True

    def write_to_file(self, link):
        with open("new.txt", "w", encoding="utf-8") as file:
            file.write(link+"\n")
            file.close()

    def wallpaper_getter(self, sub: str, limit: int):
        reddit = self.initialize_reddit_client()
        subreddit = reddit.subreddit(sub)
        hottest_post = subreddit.hot(limit=limit)
        gotten = 0

        for post in hottest_post:  # getting post submission so that I can look at the comments
            post_submission = reddit.submission(id=post.id)

            # looping over the comments
            for comments in post_submission.comments:
                # checking if the current comment has an author because people can make comments without having their names showing
                if comments.author is not None:

                    # looking for ze-robot coz that's what r/wallpaper uses. Thinking of making this a variable incase I wanna change subreddits
                    if comments.author.name == "ze-robot":
                        # Getting the body of the comments
                        body = comments.body

                        print("Trying to get a link")

                        # Complex regex just to get 1366 x 768
                        match = re.search(
                            r"\[[1-9×]+\]\([\w+://\.\-×]+\)", body)
                        if match != None:
                            start, end = match.span()
                            link = body[start:end]
                            print(link)

                            # looping over the matches even tho it's just one. I guess I need to fix this when I come online
                            # for match in m:
                            print(post.title)
                            # print("Getting an image")

                            # downloaded = self.download_file(post.title, link)
                            self.write_to_file(link)
                            gotten += 1

                        # Getting the image using requests so that we can get the raw bytes of the image
                            print("\n")

        print("-"*32, "Statistics", "-"*32)
        print(f"Tried:\t {limit}")
        print(f"Gotten:\t {gotten}")


def main():
    number = int(input("Enter the number of posts that you want to collect: "))
    origami = Origami()
    origami.wallpaper_getter("wallpaper", number)


if __name__ == "__main__":
    main()

