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
        self.prevId = set()
        self.newId = set()
        if os.path.exists("new.txt"):
            with open("new.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    self.prevId.add(line.strip())
        print(self.prevId)

    def initialize_reddit_client(self):
        reddit_authorized = praw.Reddit(
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            redirect_uri=self.REDIRECT_URI,
            # refresh_token=self.REFRESH_TOKEN,
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

    # def check_to_file(self):
    #     tempSet = set()
    #     if os.path.exists("new.txt"):
    #         with open("new.txt", "r") as file:
    #             lines = file.readlines()
    #             for line in lines:
    #                 self.prevLinks.add(line.strip())

    #     # print(self.prevLinks)
    #     if len(self.newLinks) != 0:
    #         tempSet = self.newLinks - self.prevLinks
    #     return tempSet

    def write_to_file(self):
        # tempSet = self.check_to_file()

        with open("new.txt", "a", encoding="utf-8") as file:
            for id in self.newId:
                print(f"Writing {id} to file")
                file.write(id+"\n")
            file.close()

    def get_link(self, client, id):
        post = client.submission(id)
        for comments in post.comments:  # checking if the current comment has an author because people can make comments without having their names showing
            if comments.author is not None:

                # looking for ze-robot coz that's what r/wallpaper uses. Thinking of making this a variable incase I wanna change subreddits
                if comments.author.name == "ze-robot":
                    # Getting the body of the comments
                    body = comments.body

                    # Complex regex just to get 1366 x 768
                    match = re.search(
                        r"\[[1-9×]+\]\([\w+://\.\-×]+\)", body)
                    if match != None:
                        start, end = match.span()
                        link = body[start:end]
                        link = link[11: len(link) - 1]
                        # looping over the matches even tho it's just one. I guess I need to fix this when I come online
                        # for match in m:
                        # downloaded = self.download_file(post.title, link)
                        # self.write_to_file(link)
                        print(f"Title: \t{post.title}")

                        print(f"Link: \t{link}")
                        self.newId.add(id)
                        print()
                        return True
        return False

    def wallpaper_getter(self, sub: str, limit: int):
        reddit = self.initialize_reddit_client()
        subreddit = reddit.subreddit(sub)
        # hottest_post = subreddit.hot(limit=limit)
        gotten = 0

        while gotten != limit:  # getting post submission so that I can look at the comments
            post = subreddit.random()
            print(post.id)
            if post.id in self.prevId and post.up < 1000:
                print(f"{post.id = } = {self.prevId = }")
                continue
            else:
                got = self.get_link(reddit, post.id)
                if got:
                    gotten += 1
            # looping over the comments
            print(f"{gotten = }")
            if gotten == limit:
                break
        print("-"*32, "Statitics", "-"*32)
        print(f"Tried:\t {limit}")
        print(f"Gotten:\t {gotten}")


def main():
    origami = Origami()
    origami.wallpaper_getter("wallpaper", 10)
    origami.write_to_file()


main()
