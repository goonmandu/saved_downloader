# YOU MUST MAKE A credentials.py FILE BEFOREHAND!
# PREFERABLY OF THIS FORMAT:
''' FILENAME: credentials.py
USERNAME = "YOUR REDDIT USERNAME"
PASSWORD = "YOUR REDDIT PASSWORD"
CLIENT_ID = "THE CLIENT ID FOUND IN https://www.reddit.com/prefs/apps"
SECRET = "THE CLIENT SECRET FOUND IN https://www.reddit.com/prefs/apps"
'''
# THE CODE RELIES ON IMPORTING THE VARIABLES IN IT TO FUNCTION.

# TODO: Make a log file of successes and fails and their reason

import os
import urllib.error
import wget
import requests.auth
from filter import filter_dupes_and_invalids, recursive_in
from credentials import USERNAME, PASSWORD, CLIENT_ID, SECRET


# Download alternative for HTTP 403 errors
def download_via_requests(addr, path, output_name):
    d_img = open(f"{path}/{output_name}", 'wb')
    resp = requests.get(addr, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36"
    })
    d_img.write(resp.content)
    d_img.close()


def recurse_comment_tree_and_write(outfile, comment_json):
    working = comment_json["data"]["children"]
    for item in working:
        item_data = item["data"]
        replies_exists = False
        if "body" in item_data.keys():
            text_lines = item_data["body"].split('\n')
            # TODO: I WAS TRYING TO SPLIT LINE BREAKS IN A COMMENT AND INDENT THEM
            for index, text in enumerate(text_lines):
                if index and text:
                    outfile.write('  ' * (item_data["depth"]) + text + '\n')
                elif not index and text:
                    if not item_data["depth"]:
                        outfile.write(text + '\n')
                    else:
                        outfile.write('  ' * item_data["depth"] + '└─' + text_lines[0] + '\n')
        if "replies" in item_data.keys():
            if item_data["replies"] != "":
                recurse_comment_tree_and_write(outfile, item_data["replies"])
        if item_data["depth"] == 0:
            outfile.write("\n\n")


# Define core variables
format_filter = ("jpg", "jpeg", "png", "gif")
gay_filter = ["gay", "femboy", "trap", "twink", "bisexual", "futa", "venti"]
sfw_lgbt_filter = ["egg", "lgbt", "ennnnnnnnnnnnbbbbbby"]
skip_sites = ["pximg", "gelbooru"]
allow_sites = ["redgifs", "discordapp"]
TOKEN_ACCESS_ENDPOINT = "https://www.reddit.com/api/v1/access_token"
OAUTH_ENDPOINT = "https://oauth.reddit.com"
post_num = 0

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
if not os.path.exists("comments"):
    os.mkdir("comments")

count = int(input("How many HUNDRED posts to download? (Max 10) "))
if count > 10:
    count = 10

# Authenticate App
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)
post_data = {
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD
}
headers = {
    "User-Agent": "Saved Image Downloader Beta",
}

# Get API Token
print("Getting API token... ")
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
    "User-Agent": "Saved Image Downloader Beta 2",
    "Authorization": "Bearer " + token_id
}

headers_comments = headers_get

# Begin download
print("Downloading... ")

# Download count * 100 latest images, max saved by reddit is 1000
for _ in range(count):
    # Get Posts JSON from Reddit
    response_saved = requests.get(OAUTH_ENDPOINT + f"/user/{USERNAME}/saved", headers=headers_get, params=params_get)
    post_data = response_saved.json()
    saved_count = len(post_data["data"]["children"])
    saved_list = []
    for i in range(saved_count):
        saved_list.append(post_data["data"]["children"][i]["data"])

    # Get all files in base directory, and add to list
    existing_files = []
    for root, dirs, file in os.walk(os.getcwd()):
        for name in file:
            if name.endswith(format_filter):
                existing_files.append(name)

    # Download images from source in URLs
    for post in saved_list:
        # DEBUG
        # print(post)
        # continue
        # List of image URLs in the post, appended to within this for loop
        url = []
        filename = ""

        # If the post is a gallery,
        if "gallery" in post["url"]:
            # DEBUG
            # print(post.keys())
            # If the post is a crosspost,
            if "crosspost_parent_list" in post.keys():
                # DEBUG
                # print("Crossposted")

                if post["crosspost_parent_list"][0]["media_metadata"] is None:
                    # Skip this post
                    post_num += 1
                    print(f"Skipped {post_num} of {count * 100} ({round(post_num / (count * 100) * 100, 3)}%)")
                    continue

                # Dig into crosspost parent and get media_metadata from it
                for key in post["crosspost_parent_list"][0]["media_metadata"].keys():
                    ext = post["crosspost_parent_list"][0]["media_metadata"][key]["m"].split("/")[-1]
                    # preview_url = post["crosspost_parent_list"][0]["media_metadata"][key]["o"]["u"]
                    image_url = f"https://i.redd.it/{key}.{ext}"
                    url.append(image_url)
            # If the post is NOT a crosspost,
            else:
                # DEBUG
                # print("Not a crosspost")

                # If post has been removed for some reason,
                if post["media_metadata"] is None:
                    post_num += 1
                    print(f"Skipped {post_num} of {count * 100} ({round(post_num / (count * 100) * 100, 3)}%)")
                    continue

                # Get media_metadata directly from post
                for key in post["media_metadata"].keys():
                    ext = post["media_metadata"][key]["m"].split("/")[-1]
                    # preview_url = post["crosspost_parent_list"][0]["media_metadata"][key]["o"]["u"]
                    image_url = f"https://i.redd.it/{key}.{ext}"
                    url.append(image_url)

        # If the image source is https://redgifs.com,
        elif "redgifs" in post["url"]:
            try:
                if "reddit_video_preview" in post["preview"].keys():
                    url.append(post["preview"]["reddit_video_preview"]["fallback_url"])
                else:
                    url.append(post["preview"]["images"][0]["source"]["url"].split("?")[0].replace("preview", "i"))
            except KeyError:
                # TODO: Make a log file of successes and fails and their reason
                pass
            '''
            # DEBUG
            print(post)
            # Get redgifs post ID from HTML and convert it into a scrapable direct source
            try:
                search_for = '<meta property="og:video" content="'
                html_resp = html.unescape(requests.get(post["url"]).text)
                hacky_index = html_resp.index(search_for)
                end_index = ─html_resp[hacky_index+len(search_for):].index('"')
                url.append(html_resp[hacky_index+len(search_for):hacky_index+len(search_for)+end_index])
            # If video was deleted on redgifs:
            except ValueError:
                url.append(post["preview"]["reddit_video_preview"]["fallback_url"]) 
            '''
        # If the image source is anywhere else:
        else:
            url.append(post["url"])

        # For each image URL gathered from the post,
        for entry in url:
            # DEBUG
            # print(entry)

            # Allowed sites filter, I have no idea why I added this but pretty sure the code will break without it
            if not recursive_in(allow_sites, entry) and (not entry.endswith(format_filter)
                                                         or recursive_in(skip_sites, entry)):
                break
            # Current working file name is the last item in web directory tree
            filename = entry.split("/")[-1]

            # Check if origin subreddit has certain keywords, then download the images to an appropriate folder
            # allow_sites block wget, so we need to spoof the user agent with another download function
            try:
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
            except urllib.error.HTTPError:
                pass

        # Get comment tree of each post
        post_id = post["name"].split("_")[-1]
        post_title = post["title"].replace("/", "slash").replace("\\", "backslash")
        post_subreddit = post["subreddit"]
        comments_of_post = requests.get(OAUTH_ENDPOINT + f"/comments/{post_id}", headers=headers_comments).json()[1]
        # DEBUG
        # print(str(json.dumps(comments_of_post)))
        # print(type(comments_of_post))

        if not os.path.exists(f"comments/{post_subreddit}"):
            os.mkdir(f"comments/{post_subreddit}")
        with open(f"comments/{post_subreddit}/{post_title}.txt", "w") as pc:
            pc.write(f"Relevant media: {filename}\n\n\n")
            recurse_comment_tree_and_write(pc, comments_of_post)
        post_num += 1
        print(f"Processed {post_num} of {count * 100} ({round(post_num / (count * 100) * 100, 3)}%)")

    # Add "after" parameter to get request for more than 100 downloads
    params_get["after"] = post_data["data"]["after"]
print("\nDone.")

# Filter downloaded results
do_filter = input("Perform dupe/invalid check? [y/n] ").lower()

if do_filter == "y":
    filter_dupes_and_invalids()
