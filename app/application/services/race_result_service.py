from app.application.use_cases.fetch_race_result import FetchRaceResultUseCase
from app.infrastructure.services.discord_service import DiscordService
from typing import Optional
import datetime


class RaceResultService:
    def __init__(
        self,
        fetch_race_result_use_case: FetchRaceResultUseCase,
        discord_service: Optional[DiscordService] = None,
    ):
        self.fetch_race_result_use_case = fetch_race_result_use_case
        self.discord_service = discord_service

    def format_race_result_message(self) -> str:
        race_result_collection = self.fetch_race_result_use_case.execute()

        now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)

        content = "@here "
        content += f"{str(now.month).zfill(2)}/{str(now.day).zfill(2)}(月)時点での集計結果だ！\n"

        race_results = race_result_collection.get_race_results()
        for race_result in race_results:
            content += race_result.format_result()

        content += "詳細はhttps://poginfo.ddo.jp/pogs/poginfo を確認してくれ！"

        return content

    def send_race_result_to_discord(self, enable_discord: bool = False) -> bool:
        content = self.format_race_result_message()

        if enable_discord and self.discord_service:
            return self.discord_service.post_message(content)

        return False
