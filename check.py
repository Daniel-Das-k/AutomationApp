import time
from datetime import datetime
from dateutil import parser, relativedelta

class SocialMediaScheduler:
    def schedule_post(self, platform: str, datetime_str: str, content: str):
        post_time = self.parse_time(datetime_str)
        current_time = datetime.now()

        delay = (post_time - current_time).total_seconds()
        if delay > 0:
            time.sleep(delay)

        self.post_content(platform, content)

    def parse_time(self, time_str: str) -> datetime:
        current_time = datetime.now()
        time_str = time_str.lower()

        if "today" in time_str:
            time_part = parser.parse(time_str.replace("today", "").strip(), default=current_time)
            post_time = current_time.replace(hour=time_part.hour, minute=time_part.minute, second=0, microsecond=0)
        
        elif "tomorrow" in time_str:
            time_part = parser.parse(time_str.replace("tomorrow", "").strip(), default=current_time)
            post_time = (current_time + relativedelta.relativedelta(days=1)).replace(hour=time_part.hour, minute=time_part.minute, second=0, microsecond=0)
        
        elif "next" in time_str:
            time_part = parser.parse(time_str)
            post_time = current_time + relativedelta.relativedelta(weekday=time_part.weekday(), hour=time_part.hour, minute=time_part.minute, second=0, microsecond=0)
            if post_time <= current_time:
                post_time += relativedelta.relativedelta(weeks=1)
        
        else:
            post_time = parser.parse(time_str, default=current_time)

        return post_time

    def post_content(self, platform: str, content: str):
        platform = platform.lower()
        if platform == "instagram":
            self.post_to_instagram(content)
        elif platform == "facebook":
            self.post_to_facebook(content)
        elif platform == "discord":
            self.post_to_discord(content)
        elif platform == "linkedin":
            self.post_to_linkedin(content)
        else:
            print("Unsupported platform")

    def post_to_instagram(self, content: str):
        print(f"Posting to Instagram: {content}")

    def post_to_facebook(self, content: str):
        print(f"Posting to Facebook: {content}")

    def post_to_discord(self, content: str):
        print(f"Posting to Discord: {content}")

    def post_to_linkedin(self, content: str):
        print(f"Posting to LinkedIn: {content}")

scheduler = SocialMediaScheduler()
scheduler.schedule_post('Instagram', 'today at 11:52pm', 'This is a test post for Instagram.')
