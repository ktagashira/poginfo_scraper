import os
from app.infrastructure.repositories.pog_info_scraper_repository import (
    PogInfoScraperRepository,
)
from app.application.use_cases.fetch_race_info import FetchRaceInfoUseCase
from app.application.services.race_info_service import RaceInfoService
from app.infrastructure.services.discord_service import DiscordService


if __name__ == "__main__":
    repository = PogInfoScraperRepository()
    fetch_race_info_use_case = FetchRaceInfoUseCase(repository)

    enable_discord = os.environ.get("ENABLE_DISCORD", "false").lower() == "true"
    discord_service = None
    if enable_discord:
        discord_service = DiscordService()

    race_info_service = RaceInfoService(fetch_race_info_use_case, discord_service)

    content = race_info_service.format_race_info_message()
    print(content)

    if enable_discord:
        discord_sent = race_info_service.send_race_info_to_discord(enable_discord=True)
        print(f"Discord notification sent: {discord_sent}")
