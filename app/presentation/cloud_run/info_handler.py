import json
import logging
import os
from app.infrastructure.repositories.pog_info_scraper_repository import (
    PogInfoScraperRepository,
)
from app.application.use_cases.fetch_race_info import FetchRaceInfoUseCase
from app.application.services.race_info_service import RaceInfoService
from app.infrastructure.services.discord_service import DiscordService

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def info_handler(enable_discord: bool = False):
    repository = PogInfoScraperRepository()
    fetch_race_info_use_case = FetchRaceInfoUseCase(repository)

    discord_service = None
    if enable_discord:
        discord_service = DiscordService()

    race_info_service = RaceInfoService(fetch_race_info_use_case, discord_service)

    content = race_info_service.format_race_info_message()
    logger.info(content)

    if enable_discord:
        discord_sent = race_info_service.send_race_info_to_discord(enable_discord=True)
        logger.info(f"Discord notification sent: {discord_sent}")

    return {"statusCode": 200, "body": json.dumps(content)}


if __name__ == "__main__":
    enable_discord = os.environ.get("ENABLE_DISCORD", "false").lower() == "true"
    result = info_handler(enable_discord=enable_discord)
    print(result)
