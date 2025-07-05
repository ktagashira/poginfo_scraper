from app.application.use_cases.fetch_race_info import FetchRaceInfoUseCase
from app.infrastructure.services.discord_service import DiscordService
from typing import Optional


class RaceInfoService:
    def __init__(
        self,
        fetch_race_info_use_case: FetchRaceInfoUseCase,
        discord_service: Optional[DiscordService] = None,
    ):
        self.fetch_race_info_use_case = fetch_race_info_use_case
        self.discord_service = discord_service

    def format_race_info_message(self) -> str:
        race_info_collection = self.fetch_race_info_use_case.execute()

        content = "今週出走のイかれたメンバーを紹介するぜ！\n"
        date_list = race_info_collection.get_unique_dates()

        for date in date_list:
            content += f"======{date}出走予定======\n"
            races = race_info_collection.get_races_by_date(date)
            for race in races:
                content += race.format_info()

        return content

    def send_race_info_to_discord(self, enable_discord: bool = False) -> bool:
        content = self.format_race_info_message()

        if enable_discord and self.discord_service:
            return self.discord_service.post_message(content)

        return False
