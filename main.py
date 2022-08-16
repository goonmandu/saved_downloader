# YOU MUST MAKE A credentials.py FILE BEFOREHAND!
# PREFERABLY OF THIS FORMAT:
'''
USERNAME = "YOUR REDDIT USERNAME"
PASSWORD = "YOUR REDDIT PASSWORD"
CLIENT_ID = "THE CLIENT ID FOUND IN https://www.reddit.com/prefs/apps"
SECRET = "THE CLIENT SECRET FOUND IN https://www.reddit.com/prefs/apps"
'''
# THE CODE RELIES ON IMPORTING THE VARIABLES IN IT TO FUNCTION.

import os
import wget
import shutil
import requests.auth
from credentials import USERNAME, PASSWORD, CLIENT_ID, SECRET


def recursive_in(filter, string):
    for entry in filter:
        if entry.lower() in string.lower():
            return True
    return False


TOKEN_ACCESS_ENDPOINT = "https://www.reddit.com/api/v1/access_token"

# Authenticate App
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)
post_data = {
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD
}
headers = {
    "User-Agent": "Saved Image Downloader Beta 1"
}

# Get API Token
print("Getting API token...")
response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)
if response.status_code == 200:
    token_id = response.json()["access_token"]
    print("Done.")
else:
    token_id = ""

OAUTH_ENDPOINT = "https://oauth.reddit.com"
params_get = {
    "limit": 250
}
headers_get = {
    "User-Agent": "Saved Image Downloader Alpha 1",
    "Authorization": "Bearer " + token_id
}

response_saved = requests.get(OAUTH_ENDPOINT + f"/user/{USERNAME}/saved", headers=headers_get, params=params_get)
data = response_saved.json()
saved_count = len(data["data"]["children"])
saved_list = []
format_filter = ("jpg", "jpeg", "png", "gif")
gay_filter = ["gay", "femboy", "trap", "twink", "bisexual"]
sfw_lgbt_filter = ["egg", "lgbt", "ennnnnnnnnnnnbbbbbby"]

if not os.path.exists("downloaded"):
    os.mkdir("downloaded")
if not os.path.exists("downloaded/gay"):
    os.mkdir("downloaded/gay")
if not os.path.exists("downloaded/straight"):
    os.mkdir("downloaded/straight")
if not os.path.exists("downloaded/sfw"):
    os.mkdir("downloaded/sfw")
if not os.path.exists("filtered"):
    os.mkdir("filtered")

for i in range(saved_count):
    saved_list.append(data["data"]["children"][i]["data"])

existing_files = []

for root, dirs, file in os.walk(os.getcwd()):
    for name in file:
        if name.endswith(format_filter):
            existing_files.append(name)

for post in saved_list:
    filename = post["url"].split("/")[-1]
    if filename.endswith(format_filter) and filename not in existing_files:
        if recursive_in(gay_filter, post["subreddit"]):
            wget.download(post["url"], f"downloaded/gay/{filename}")
        if recursive_in(sfw_lgbt_filter, post["subreddit"]):
            wget.download(post["url"], f"downloaded/sfw/{filename}")
        else:
            wget.download(post["url"], f"downloaded/straight/{filename}")

# TODO: Filter out invalid images
'''
for filename in os.listdir("downloaded"):
    if os.path.getsize(f"downloaded/{filename}") < 4096:
        shutil.move(f"downloaded/{filename}", f"filtered/{filename}")
'''