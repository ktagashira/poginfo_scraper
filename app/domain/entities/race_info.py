from pydantic import BaseModel, Field
from typing import List
import pandas as pd


class RaceInfo(BaseModel):
    horse_name: str = Field(..., description="馬名")
    race_name: str = Field(..., description="レース名")
    date: str = Field(..., description="出走日")
    time: str = Field(..., description="時刻")
    place: str = Field(..., description="場")
    round: str = Field(..., description="R")
    course: str = Field(..., description="コース")
    owner: str = Field(..., description="PO")
    jockey: str = Field(..., description="騎手")

    @property
    def condition(self) -> str:
        return f"{self.place}{self.round}R {self.course}"

    def format_info(self) -> str:
        return f"\t{self.horse_name} {self.race_name} {self.condition} 出走時刻:{self.time} 指名者: {self.owner}\n"


class RaceInfoCollection(BaseModel):
    data: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

    def get_race_infos(self) -> List[RaceInfo]:
        race_infos = []
        for _, row in self.data.iterrows():
            race_info = RaceInfo(
                horse_name=row["馬名"],
                race_name=row["ﾚｰｽ名"],
                date=row["出走日"],
                time=row["時刻"],
                place=row["場"],
                round=row["R"],
                course=row["ｺｰｽ"],
                owner=row["PO"],
                jockey=row["騎手"],
            )
            race_infos.append(race_info)
        return race_infos

    def get_unique_dates(self) -> List[str]:
        return sorted(
            set(self.data["出走日"].tolist()),
            key=self.data["出走日"].tolist().index,
        )

    def get_races_by_date(self, date: str) -> List[RaceInfo]:
        filtered_data = self.data[self.data["出走日"] == date]
        race_infos = []
        for _, row in filtered_data.iterrows():
            race_info = RaceInfo(
                horse_name=row["馬名"],
                race_name=row["ﾚｰｽ名"],
                date=row["出走日"],
                time=row["時刻"],
                place=row["場"],
                round=row["R"],
                course=row["ｺｰｽ"],
                owner=row["PO"],
                jockey=row["騎手"],
            )
            race_infos.append(race_info)
        return race_infos
