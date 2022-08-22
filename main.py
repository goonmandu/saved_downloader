# YOU MUST MAKE A credentials.py FILE BEFOREHAND!
# PREFERABLY OF THIS FORMAT:
''' FILENAME: credentials.py
USERNAME = "YOUR REDDIT USERNAME"
PASSWORD = "YOUR REDDIT PASSWORD"
CLIENT_ID = "THE CLIENT ID FOUND IN https://www.reddit.com/prefs/apps"
SECRET = "THE CLIENT SECRET FOUND IN https://www.reddit.com/prefs/apps"
'''
# THE CODE RELIES ON IMPORTING THE VARIABLES IN IT TO FUNCTION.

import os
import wget
import html
import shutil
import requests.auth
from credentials import USERNAME, PASSWORD, CLIENT_ID, SECRET


def recursive_in(filter, string):
    for entry in filter:
        if entry.lower() in string.lower():
            return True
    return False


# Probably will be used later as a wget.download alternative
def download_via_requests(addr, path, output_name):
    d_img = open(f"{path}/{output_name}", 'wb')
    resp = requests.get(addr, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36"
    })
    d_img.write(resp.content)
    d_img.close()


# Define core variables
format_filter = ("jpg", "jpeg", "png", "gif")
gay_filter = ["gay", "femboy", "trap", "twink", "bisexual", "futa", "venti"]
sfw_lgbt_filter = ["egg", "lgbt", "ennnnnnnnnnnnbbbbbby"]
skip_sites = ["pximg", "gelbooru"]
allow_sites = ["redgifs", "discordapp"]
TOKEN_ACCESS_ENDPOINT = "https://www.reddit.com/api/v1/access_token"
OAUTH_ENDPOINT = "https://oauth.reddit.com"

# Create directory structure
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

count = int(input("How many HUNDRED posts to download? (3 means 300) "))

# Authenticate App
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)
post_data = {
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD
}
headers = {
    "User-Agent": "Saved Image Downloader Alpha 1",
}

# Get API Token
print("Getting API token...")
response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)
if response.status_code == 200:
    token_id = response.json()["access_token"]
    print("Done.")
else:
    token_id = 0
    print("FATAL: Failed to get API token.")
    exit(1)

params_get = {
    "limit": 100
}

headers_get = {
    "User-Agent": "Saved Image Downloader Beta 1",
    "Authorization": "Bearer " + token_id
}
print("Downloading...")
# Get 5 * 100 = 500 latest saved posts
for _ in range(count):
    response_saved = requests.get(OAUTH_ENDPOINT + f"/user/{USERNAME}/saved", headers=headers_get, params=params_get)
    data = response_saved.json()
    saved_count = len(data["data"]["children"])
    saved_list = []
    for i in range(saved_count):
        saved_list.append(data["data"]["children"][i]["data"])

    existing_files = []

    for root, dirs, file in os.walk(os.getcwd()):
        for name in file:
            if name.endswith(format_filter):
                existing_files.append(name)

    for post in saved_list:
        url = []
        if "gallery" in post["url"] and post["media_metadata"] is not None:
            for key in post["media_metadata"].keys():
                preview_url = post["media_metadata"][key]["s"]["u"]
                image_url = preview_url.replace("preview", "i").split("?")[0]
                url.append(image_url)
        elif "redgifs" in post["url"]:
            search_for = '<meta property="og:video" content="'
            html_resp = html.unescape(requests.get(post["url"]).text)
            hacky_index = html_resp.index(search_for)
            end_index = html_resp[hacky_index+len(search_for):].index('"')
            url.append(html_resp[hacky_index+len(search_for):hacky_index+len(search_for)+end_index])
        else:
            url.append(post["url"])

        for entry in url:
            if not recursive_in(allow_sites, entry) and (not entry.endswith(format_filter) or recursive_in(skip_sites, entry)):
                break
            filename = entry.split("/")[-1]
            if recursive_in(gay_filter, post["subreddit"]):
                if recursive_in(allow_sites, entry):
                    download_via_requests(entry, "downloaded/gay", filename)
                elif filename not in existing_files:
                    wget.download(entry, f"downloaded/gay/{filename}")
            elif recursive_in(sfw_lgbt_filter, post["subreddit"]):
                if recursive_in(allow_sites, entry):
                    download_via_requests(entry, "downloaded/sfw", filename)
                elif filename not in existing_files:
                    wget.download(entry, f"downloaded/sfw/{filename}")
            else:
                if recursive_in(allow_sites, entry):
                    download_via_requests(entry, "downloaded/straight", filename)
                elif filename not in existing_files:
                    wget.download(entry, f"downloaded/straight/{filename}")
    params_get["after"] = data["data"]["after"]
print("\nDone.")


# TODO: Filter out invalid images
'''
print("Filtering invalid files...")
for filename in os.listdir("downloaded"):
    if os.path.getsize(f"downloaded/{filename}") < 4096:
        shutil.move(f"downloaded/{filename}", f"filtered/{filename}")
print("Done.")
'''