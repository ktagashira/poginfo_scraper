from abc import ABC, abstractmethod
import pandas as pd


class RaceInfoRepository(ABC):
    @abstractmethod
    def fetch_race_information(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def fetch_race_result(self) -> pd.DataFrame:
        pass
