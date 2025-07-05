import os
from app.infrastructure.repositories.pog_info_scraper_repository import (
    PogInfoScraperRepository,
)
from app.application.use_cases.fetch_race_result import FetchRaceResultUseCase
from app.application.services.race_result_service import RaceResultService
from app.infrastructure.services.discord_service import DiscordService


if __name__ == "__main__":
    repository = PogInfoScraperRepository()
    fetch_race_result_use_case = FetchRaceResultUseCase(repository)

    enable_discord = os.environ.get("ENABLE_DISCORD", "false").lower() == "true"
    discord_service = None
    if enable_discord:
        discord_service = DiscordService()

    race_result_service = RaceResultService(fetch_race_result_use_case, discord_service)

    content = race_result_service.format_race_result_message()
    print(content)

    if enable_discord:
        discord_sent = race_result_service.send_race_result_to_discord(
            enable_discord=True
        )
        print(f"Discord notification sent: {discord_sent}")
