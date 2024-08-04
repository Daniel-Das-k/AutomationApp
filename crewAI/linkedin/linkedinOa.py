
# import os
# import json
# from requests_oauthlib import OAuth2Session

# # Set environment variables
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# # Credentials you get from registering a new application
# client_id = '86n58yur6d34hr'
# client_secret = 'Ri8Tqzsxly7CbBGm'

# # LinkedIn OAuth2 requests require scope and redirect_url parameters.
# # Ensure these values match the auth values in your LinkedIn App
# # (see auth tab on LinkedIn Developer page)
# scope = ['email,openid,profile,w_member_social']
# redirect_url = 'http://127.0.0.1:8000/accounts/linkedin_oauth2/login/callback/'

# # OAuth endpoints given in the LinkedIn API documentation
# authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
# token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

# linkedin = OAuth2Session(client_id, redirect_uri=redirect_url, scope=scope)

# # Redirect user to LinkedIn for authorization
# authorization_url, state = linkedin.authorization_url(authorization_base_url)
# print(f"Please go here and authorize: {authorization_url}")

# # Get the authorization verifier code from the callback URL
# redirect_response = input('Paste the full redirect URL here:')

# # Fetch the access token
# token = linkedin.fetch_token(token_url, client_secret=client_secret,
#                              include_client_id=True,
#                              authorization_response=redirect_response)

# # Store the access token in a JSON file
# with open('linkedin_token.json', 'w') as token_file:
#     json.dump(token, token_file)

# # Fetch a protected resource, i.e., user profile
# r = linkedin.get('https://api.linkedin.com/v2/userinfo')
# print(r.content)

import os
import json
from requests_oauthlib import OAuth2Session

# Set environment variables
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Credentials you get from registering a new application
client_id = '86n58yur6d34hr'
client_secret = 'Ri8Tqzsxly7CbBGm'

# LinkedIn OAuth2 requests require scope and redirect_url parameters.
# Ensure these values match the auth values in your LinkedIn App
# (see auth tab on LinkedIn Developer page)
scope = ['email,openid,profile,w_member_social']
redirect_url = 'http://127.0.0.1:8000/accounts/linkedin_oauth2/login/callback/'

# OAuth endpoints given in the LinkedIn API documentation
authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

linkedin = OAuth2Session(client_id, redirect_uri=redirect_url, scope=scope)

# Redirect user to LinkedIn for authorization
authorization_url, state = linkedin.authorization_url(authorization_base_url)
print(f"Please go here and authorize: {authorization_url}")

# Get the authorization verifier code from the callback URL
redirect_response = input('Paste the full redirect URL here:')

# Fetch the access token
token = linkedin.fetch_token(token_url, client_secret=client_secret,
                             include_client_id=True,
                             authorization_response=redirect_response)

# Store the access token in a JSON file
with open('linkedin_token.json', 'w') as token_file:
    json.dump(token, token_file)

# Fetch a protected resource, i.e., user profile
r = linkedin.get('https://api.linkedin.com/v2/userinfo')
print(r.content)

# Post a sample text post
post_url = 'https://api.linkedin.com/rest/posts'
post_headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token["access_token"]}',
    'X-Restli-Protocol-Version': '2.0.0',
    'LinkedIn-Version': '202306'  # Add the required version header
}
post_data = {
  "author": "urn:li:organization:5515715",
  "commentary": "Sample text Post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": False
}

response = linkedin.post(post_url, headers=post_headers, json=post_data)

print('Post response:', response.json())
