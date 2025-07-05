import json
import logging
import os
from app.infrastructure.repositories.pog_info_scraper_repository import (
    PogInfoScraperRepository,
)
from app.application.use_cases.fetch_race_result import FetchRaceResultUseCase
from app.application.services.race_result_service import RaceResultService
from app.infrastructure.services.discord_service import DiscordService

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def result_handler(enable_discord: bool = False):
    repository = PogInfoScraperRepository()
    fetch_race_result_use_case = FetchRaceResultUseCase(repository)

    discord_service = None
    if enable_discord:
        discord_service = DiscordService()

    race_result_service = RaceResultService(fetch_race_result_use_case, discord_service)

    content = race_result_service.format_race_result_message()
    logger.info(content)

    if enable_discord:
        discord_sent = race_result_service.send_race_result_to_discord(
            enable_discord=True
        )
        logger.info(f"Discord notification sent: {discord_sent}")

    return {"statusCode": 200, "body": json.dumps(content)}


if __name__ == "__main__":
    enable_discord = os.environ.get("ENABLE_DISCORD", "false").lower() == "true"
    result = result_handler(enable_discord=enable_discord)
    print(result)
