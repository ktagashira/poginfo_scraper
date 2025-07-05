from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os
import uuid
import logging
import time

POG_INFO_LOGIN_URL = "https://poginfo.ddo.jp/pogs/login/"

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PogInfoScraper:
    def __init__(self):
        logger.info("Initializing PogInfoScraper")
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-dev-tools")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")

            unique_dir = f"/tmp/chrome_user_data_{uuid.uuid4()}"
            options.add_argument(f"--user-data-dir={unique_dir}")
            logger.info(f"Chrome user data directory: {unique_dir}")

            logger.info("Starting Chrome WebDriver...")
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_page_load_timeout(60)
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("Chrome WebDriver started successfully")
        except Exception as e:
            logger.error(f"Chrome WebDriver initialization error: {e}")
            raise

    def login(self):
        logger.info("Starting login process")
        try:
            logger.info(f"Accessing POGINFO site: {POG_INFO_LOGIN_URL}")
            self.driver.get(POG_INFO_LOGIN_URL)
            
            # Wait for page to be fully loaded
            self.wait.until(EC.presence_of_element_located((By.NAME, "poginfoTeamId")))
            logger.info("Page loaded successfully")

            logger.info("Searching for login form elements...")
            login_form_group = self.driver.find_element(By.NAME, value="poginfoTeamId")
            login_form_id = self.driver.find_element(By.NAME, value="poginfoMemberId")
            login_form_password = self.driver.find_element(By.NAME, value="poginfoPassword")
            logger.info("Login form elements found")

            logger.info("Entering login credentials...")
            login_form_group.send_keys(os.environ["GROUP_NAME"])
            login_form_id.send_keys(os.environ["USER_ID"])
            login_form_password.send_keys(os.environ["PASSWORD"])
            logger.info("Login credentials entered")

            logger.info("Waiting for login button to be clickable...")
            submit_button = self.wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
            logger.info("Clicking login button")
            self.driver.execute_script("arguments[0].click();", submit_button)
            time.sleep(3)  # Wait for login process
            logger.info("Login process completed")
        except TimeoutException as e:
            logger.error(f"Login timeout error: {e}")
            raise
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise

    def fetch_race_information(self) -> pd.DataFrame:
        logger.info("Starting race information fetch")
        try:
            self.login()
            
            logger.info("Clicking race information menu...")
            menu_elements = self.driver.find_elements(By.CSS_SELECTOR, value=".col-4")
            logger.info(f"Found {len(menu_elements)} menu elements")
            
            # Wait for menu element to be clickable and click it
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-4")))
            menu_elements[1].click()
            logger.info("Race information menu clicked")

            logger.info("Searching for race information table...")
            # Wait for the table to be present after navigation
            self.wait.until(EC.presence_of_element_located((By.ID, "tableList")))
            race_information_table_elm = self.driver.find_element(By.ID, value="tableList")
            logger.info("Race information table found")
            
            logger.info("Parsing race information table...")
            parsed_race_information = self.parse_table(race_information_table_elm)
            logger.info(f"Parsed {len(parsed_race_information)} race information rows")

            return parsed_race_information
        except TimeoutException as e:
            logger.error(f"Race information fetch timeout error: {e}")
            raise
        except Exception as e:
            logger.error(f"Race information fetch error: {e}")
            raise

    def fetch_race_result(self) -> pd.DataFrame:
        logger.info("Starting race result fetch")
        try:
            self.login()
            
            logger.info("Clicking race result menu...")
            menu_elements = self.driver.find_elements(By.CSS_SELECTOR, value=".col-4")
            logger.info(f"Found {len(menu_elements)} menu elements")
            
            # Wait for menu element to be clickable and click it
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-4")))
            menu_elements[0].click()
            logger.info("Race result menu clicked")

            logger.info("Searching for race result table...")
            # Wait for the table to be present after navigation
            self.wait.until(EC.presence_of_element_located((By.ID, "tableList")))
            race_result_table_elm = self.driver.find_element(By.ID, value="tableList")
            logger.info("Race result table found")
            
            logger.info("Parsing race result table...")
            parsed_race_result = self.parse_table(race_result_table_elm)
            logger.info(f"Parsed {len(parsed_race_result)} race result rows")

            return parsed_race_result
        except TimeoutException as e:
            logger.error(f"Race result fetch timeout error: {e}")
            raise
        except Exception as e:
            logger.error(f"Race result fetch error: {e}")
            raise

    def parse_table(self, table_elm: WebElement) -> pd.DataFrame:
        logger.info("Starting table parsing")
        try:
            logger.info("Extracting table headers...")
            theads = (
                table_elm.find_element(By.TAG_NAME, value="thead")
                .find_element(By.TAG_NAME, value="tr")
                .find_elements(By.TAG_NAME, value="th")
            )
            cols = [th.text.replace("\n", "") for th in theads]
            logger.info(f"Found {len(cols)} columns: {cols}")

            logger.info("Extracting table body...")
            tbodies = table_elm.find_element(By.TAG_NAME, value="tbody").find_elements(
                By.TAG_NAME, value="tr"
            )
            logger.info(f"Found {len(tbodies)} table rows")

            tb_list = []
            for tb in tbodies:
                tmp_list = []
                tbody = tb.find_elements(By.TAG_NAME, value="td")
                for td in tbody:
                    tmp_list.append(td.text)
                tb_list.append(tmp_list)

            df = pd.DataFrame(tb_list, columns=cols)
            logger.info(f"Created DataFrame with shape: {df.shape}")

            return df
        except Exception as e:
            logger.error(f"Table parsing error: {e}")
            raise
