from app.domain.repositories.race_info_repository import RaceInfoRepository
from app.domain.entities.race_result import RaceResultCollection


class FetchRaceResultUseCase:
    def __init__(self, repository: RaceInfoRepository):
        self.repository = repository

    def execute(self) -> RaceResultCollection:
        race_data = self.repository.fetch_race_result()
        return RaceResultCollection(data=race_data)
