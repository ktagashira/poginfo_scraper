from pydantic import BaseModel, Field
from typing import List
import pandas as pd


class RaceResult(BaseModel):
    owner: str = Field(..., description="PO")
    income: str = Field(..., description="収支")
    last_income: str = Field(..., description="先週")
    rank: int = Field(..., description="順位")

    def format_result(self) -> str:
        return f"\t{self.rank}位:　{self.owner} {self.income} (+{self.last_income})\n"


class RaceResultCollection(BaseModel):
    data: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

    def get_race_results(self) -> List[RaceResult]:
        race_results = []
        for idx, row in self.data.iterrows():
            race_result = RaceResult(
                owner=row["PO"],
                income=row["収支"],
                last_income=row["先週"],
                rank=idx + 1,
            )
            race_results.append(race_result)
        return race_results
