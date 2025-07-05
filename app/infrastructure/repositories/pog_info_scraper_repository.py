from app.domain.repositories.race_info_repository import RaceInfoRepository
from app.infrastructure.scraper.pog_info_scraper import PogInfoScraper
import pandas as pd


class PogInfoScraperRepository(RaceInfoRepository):
    def __init__(self):
        self.scraper = PogInfoScraper()

    def fetch_race_information(self) -> pd.DataFrame:
        return self.scraper.fetch_race_information()

    def fetch_race_result(self) -> pd.DataFrame:
        return self.scraper.fetch_race_result()
