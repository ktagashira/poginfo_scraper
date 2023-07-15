from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd

import os

POG_INFO_LOGIN_URL = "https://poginfo.ddo.jp/pogs/login/"


class PogInfoScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/chrome/chrome"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")

        self.driver = webdriver.Chrome(
            options=options, executable_path="/opt/chromedriver"
        )
        self.driver.implicitly_wait(10)

    def login(self):
        self.driver.get(POG_INFO_LOGIN_URL)

        login_form_group = self.driver.find_element(By.NAME, value="groupid")
        login_form_id = self.driver.find_element(By.NAME, value="userid")
        login_form_password = self.driver.find_element(By.NAME, value="password")

        login_form_group.send_keys(os.environ["GROUP_NAME"])
        login_form_id.send_keys(os.environ["USER_ID"])
        login_form_password.send_keys(os.environ["PASSWORD"])

        self.driver.find_element(By.NAME, value="submit").click()

    def fetch_race_information(self) -> pd.DataFrame:
        self.login()
        self.driver.find_elements(By.CSS_SELECTOR, value=".col-4")[1].click()

        race_information_table_elm = self.driver.find_element(By.ID, value="tableList")
        parsed_race_information = self.parse_table(race_information_table_elm)

        return parsed_race_information

    def fetch_race_result(self) -> pd.DataFrame:
        self.login()
        self.driver.find_elements(By.CSS_SELECTOR, value=".col-4")[4].click()

        race_information_table_elm = self.driver.find_element(By.ID, value="tableList")
        parsed_race_result = self.parse_table(race_information_table_elm)

        return parsed_race_result

    def parse_table(self, table_elm: WebElement) -> pd.DataFrame:
        theads = (
            table_elm.find_element(By.TAG_NAME, value="thead")
            .find_element(By.TAG_NAME, value="tr")
            .find_elements(By.TAG_NAME, value="th")
        )
        cols = [th.text.replace("\n", "") for th in theads]

        tbodies = table_elm.find_element(By.TAG_NAME, value="tbody").find_elements(
            By.TAG_NAME, value="tr"
        )

        tb_list = []
        for idx, tb in enumerate(tbodies):
            tmp_list = []
            tbody = tb.find_elements(By.TAG_NAME, value="td")
            for td in tbody:
                tmp_list.append(td.text)
            tb_list.append(tmp_list)

        df = pd.DataFrame(tb_list, columns=cols)

        return df
