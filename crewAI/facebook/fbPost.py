import facebook
import json
from datetime import datetime, timedelta
import time
from crew import Facebook

fb = Facebook()
class FacebookManager:
    def __init__(self):
        self.credentials = self._load_credentials()
        self.facebook_api = self._initialize_facebook_api()

    def _load_credentials(self):
        with open('facebook_token.json', 'r') as file:
            return json.load(file)
        

    def _initialize_facebook_api(self):
        access_token = self.credentials['page_access_token']
        print(access_token)
        return facebook.GraphAPI(access_token)

    def schedule_post(self, content: str, datetime_str: str):
        post_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        current_time = datetime.now()

        delay = (post_time - current_time).total_seconds()
        if delay > 0:
            time.sleep(delay)

        self._post_to_facebook(content)

    def _post_to_facebook(self, content: str):
        try:
            text = fb.run(content)
            print(text)
            post = self.facebook_api.put_object(parent_object='me', connection_name='feed', message=text)
            print("Posting facebook....",post)
            # image = self.facebook_api.put_photo(image=open('img.png', 'rb'),
            #     message="look at this photooo...")
        except facebook.GraphAPIError as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    facebook_manager = FacebookManager()
    facebook_manager._post_to_facebook('god is great')
