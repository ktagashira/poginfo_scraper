import os
import json
import requests
from typing import Optional


class DiscordService:
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.environ.get("DISCORD_WEBHOOK_URL")

    def post_message(self, content: str) -> bool:
        if not self.webhook_url:
            raise ValueError("Discord webhook URL is not set")

        message = {"content": content}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                self.webhook_url, json.dumps(message), headers=headers
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Discord message: {e}")
            return False
