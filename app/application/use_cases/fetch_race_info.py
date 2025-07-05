from app.domain.repositories.race_info_repository import RaceInfoRepository
from app.domain.entities.race_info import RaceInfoCollection


class FetchRaceInfoUseCase:
    def __init__(self, repository: RaceInfoRepository):
        self.repository = repository

    def execute(self) -> RaceInfoCollection:
        race_data = self.repository.fetch_race_information()
        return RaceInfoCollection(data=race_data)
