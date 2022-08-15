# YOU MUST MAKE A credentials.py FILE BEFOREHAND!
# PREFERABLY OF THIS FORMAT:
'''
USERNAME = "YOUR REDDIT USERNAME"
PASSWORD = "YOUR REDDIT PASSWORD"
CLIENT_ID = "THE CLIENT ID FOUND IN https://www.reddit.com/prefs/apps"
SECRET = "THE CLIENT SECRET FOUND IN https://www.reddit.com/prefs/apps"
'''
# THE CODE RELIES ON IMPORTING THE VARIABLES IN IT TO FUNCTION.

import requests.auth
from credentials import USERNAME, PASSWORD, CLIENT_ID, SECRET

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
response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)
if response.status_code == 200:
    token_id = response.json()["access_token"]
else:
    token_id = ""

OAUTH_ENDPOINT = "https://oauth.reddit.com"
params_get = {
    "limit": 69
}
headers_get = {
    "User-Agent": "Saved Image Downloader Alpha 1",
    "Authorization": "Bearer " + token_id
}
response_saved = requests.get(OAUTH_ENDPOINT + f"/user/{USERNAME}/saved", headers=headers_get, params=params_get)
data = response_saved.json()
saved_count = len(data["data"]["children"])
saved_list = []
for i in range(saved_count):
    saved_list.append(data["data"]["children"][i]["data"]["url"])
print(saved_list)