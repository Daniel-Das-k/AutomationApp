import requests
from dotenv import load_dotenv
import os
# from text import posttext
load_dotenv()

user=str(input('user name pls--'))
with open("details", "r") as f:
    for line in f:
        if line.strip().startswith(f"access_token({user})"):
            access_token = line.strip().split("=")[1]
        elif line.strip().startswith(f"id({user})"):
            id = line.strip().split("=")[1]

post_url = "https://api.linkedin.com/v2/ugcPosts"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}


post_data = {
    "author": f"urn:li:person:{id}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Second post "
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

try:
    response = requests.post(post_url, headers=headers, json=post_data)
    response.raise_for_status()  
    print("Post response:", response.json())
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    if response.content:
        print("Response content:", response.content)

except Exception as err:
    print(f"Other error occurred: {err}")
