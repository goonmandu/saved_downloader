# Reddit Saved Image Downloader  
A script that automatically downloads your saved images on Reddit.

# Requirements
Tested on Python 3.9.  
`pip install wget`  
`pip install requests`

# If you want to use this:
## Registering the Reddit app
1. Go to https://www.reddit.com/prefs/apps and click on "create another app..."  
2. Name: Anything you want.
3. Developer: **Your Reddit username.**
4. Select the "script" radio button.
5. Description: Anything you want.
6. About URL: **Leave blank.**
7. Redirect URI: `http://localhost:` + `Any port number`.
8. Click on "create app."
## Entering in the credentials
1. Make a `credentials.py` file in the same directory as `main.py`.
2. Structure the file in this manner:  
```py
USERNAME = "Your Reddit username"
PASSWORD = "Your Reddit password"
CLIENT_ID = "Your app's client ID. Found under 'personal use script.'"
SECRET = "Your app's client secret. Found above the app name."
```
## Run
```bash
~$ python3 main.py
```

# TODO
- [x] Download images in gallery  
- [x] Categorize images based on origin subreddit  
- [ ] Filter out files less than 4kB in size for manual review  
- [ ] Add support for command line arguments