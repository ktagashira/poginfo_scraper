import json
import sys
import logging

sys.path.append("./src")
from pog_info_scraper import PogInfoScraper

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def info_handler(event, context):
    scraper = PogInfoScraper()
    race_information = scraper.fetch_race_information()

    content = ""
    content += "今週出走のイかれたメンバーを紹介するぜ！\n"
    date_list = sorted(
        set(race_information["出走日"].tolist()),
        key=race_information["出走日"].tolist().index,
    )

    for date in date_list:
        content += "======{}出走予定======\n".format(date)
        for idx, row in race_information[race_information["出走日"] == date].iterrows():
            horse = row["馬名"]
            start_time = row["時刻"]
            race = row["ﾚｰｽ名"]
            owner = row["PO"]
            jockey = row["騎手"]
            condition = row["場"] + row["R"] + "R " + row["ｺｰｽ"]
            _content = "\t{} {} {} 出走時刻:{} 指名者: {}\n".format(
                horse, race, condition, start_time, owner
            )
            content += _content

    logger.info(content)

    return {"statusCode": 200, "body": json.dumps(content)}
