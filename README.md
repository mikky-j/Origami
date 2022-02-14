# Origami

Origami is a web scraper that get's wallpaper from any subreddit and set its as your wallpaper.

# Steps needed to set Origami up

1. First you need to set up a reddit app

   - Go to `https://reddit.com/prefs/apps`
   - Then you want to create new app
   - You will then have to give it a name, _it can be any name that you want_
     and a redirect uri of `http://localhost:8080`
   - You see your app once you are done creating it, take note of the CLIENT_ID
     (which will be directly under the name of you app),
     the SECRET_KEY and the USER_AGENT (which is just the name of your app)

2. First you need to create an `.env` file which will contain all the things that you need to set up Origami

   - You need to define the `CLIENT_ID`, `CLIENT_SECRET`, `USER_AGENT`, `REDIRECT_URI`

   ```
   CLIENT_ID=YOUR-CLIENT-ID
   CLIENT_SECRET=YOUR-CLIENT-SECRET
   REDIRECT_URI=YOUR-REDIRECT-URI
   USER_AGENT=YOUR-USER-AGENT
   ```

3. And you are done. 😎😎😎😎😎

# Setting up the folder that would change the wallpapers

## Linux

### Manjaro

1. Go to System Settings > Quick Settings > Change Wallpaper

2. Change the the wallpaper type to slideshow and then select a destionation folder
