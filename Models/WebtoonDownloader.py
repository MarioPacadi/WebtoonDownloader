import io
import json
import logging
import os
import time
import uuid
from abc import abstractmethod, ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List

import requests
from PIL import Image
from bs4 import BeautifulSoup
from dataclasses_json import dataclass_json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Models.CustomLogging import CustomLogging
from Models.LoadingBar import start_loading, done_loading
from Models.Settings import Settings
import Models.Constants as Constants


@dataclass_json
@dataclass
class WebtoonsDownloader(ABC):
    id_webtoon: str
    starting_url: str
    current_chapter: int
    folder_path: str
    name: str
    icon_path: str

    def __init__(self,
                 id_webtoon: str = str(uuid.uuid4()),
                 starting_url: str = "",
                 folder_path: str = "",
                 current_chapter: int = 1,
                 name: str = "",
                 icon_path: str = "./assets/ScraperPlaceholder.png"):
        self.id_webtoon = id_webtoon
        self.starting_url = starting_url
        self.current_chapter = current_chapter
        self.folder_path = folder_path
        self.name = name
        self.icon_path = icon_path

    def start_downloading(self):
        next_url = self.starting_url
        while next_url:
            try:
                html_content = self._download_html(next_url)
                image_links, next_url, folder_name = self._parse_html(html_content)

                full_folder_path = os.path.join(self.folder_path, folder_name)
                if not os.path.exists(full_folder_path):
                    os.makedirs(full_folder_path, exist_ok=True)
                logging.info(f"Currently processing: {folder_name}")
                self._download_images(image_links, self.folder_path, folder_name)
                if next_url:
                    logging.info(f"Moving to \"{next_url}\"")
                else:
                    logging.info(f"Webtoon download complete. Total chapters downloaded: {self.current_chapter}")
                self.current_chapter += 1
            except Exception as e:
                logging.error(e)

    # Chromedriver download site: https://googlechromelabs.github.io/chrome-for-testing/#stable
    # npx @puppeteer/browsers install chrome@stable

    def _download_html(self, url):
        html_content = ""
        try:
            start_loading("Downloading HTML")
            with open("./repo/settings.json", 'r+', encoding='utf-8') as f:
                json_str = json.load(f)
            settings = Settings.from_json(json_str)

            options = webdriver.ChromeOptions()
            options.binary_location = settings.browser_path
            # options.add_argument("--headless=new")  # Run Chrome in headless mode
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            if settings.run_in_incognito:
                options.add_argument("--incognito")  # Run Chrome in incognito mode

            options.add_argument(f"--user-agent={settings.user_agent}")  # Add user-agent to the options

            logging.info(f"Getting html from: {url}")
            # service = Service(executable_path=ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
            # service = Service(executable_path=settings.driver_path)

            Constants.global_driver = webdriver.Chrome(options=options)
            # with webdriver.Chrome(options=options) as driver:
            #     driver.get(url)
            #     self._execute_user_simulated_interaction(driver)
            #     html_content = driver.page_source

            Constants.global_driver.get(url)
            self._execute_user_simulated_interaction(Constants.global_driver)
            html_content = Constants.global_driver.page_source
            Constants.global_driver.close()
            # driver.close()
            done_loading()
        except Exception as e:
            done_loading()
            logging.error(e)

        return html_content

    def _execute_user_simulated_interaction(self, driver):
        # Wait for all images to load before getting the page source
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
        time.sleep(2)  # Wait for 2 seconds to ensure all images are loaded

    @abstractmethod
    def _parse_html(self, html_content):
        pass

    @staticmethod
    def _download_images(image_links, parent_folder, folder_name):
        if not image_links:
            logging.log(logging.WARNING, "No images found for this chapter.")
            return

        for idx, link in enumerate(image_links):
            image_name = f"{folder_name} - image{idx + 1}.jpg"
            file_path = os.path.join(parent_folder, folder_name, image_name)

            if os.path.exists(file_path):
                logging.log(logging.WARNING, f"Image \"{image_name}\" already exists. Skipping download.")
                continue

            with requests.get(link) as r:
                if r.status_code == 200:
                    with io.BytesIO(r.content) as f:
                        try:
                            img = Image.open(f)
                            img.convert("RGB").save(file_path, "JPEG")
                            logging.log(CustomLogging.SHOWCASE.value, f"Downloaded \"{link}\" to \"{file_path}\"")
                        except Exception as e:
                            print(f"Failed to convert image: {e}")
                else:
                    print(f"Failed to download image {image_name}.")

    # Helper functions

    @staticmethod
    def _clean_folder_name(folder_name):
        # Folders must not use symbols \/:*?"<>|
        folder_name = folder_name.strip().replace(":", " -")
        folder_name = folder_name.strip().replace("\n", " ")
        replacements = ['\\', "/", "*", "?", "<", ">", "|"]
        for replacement in replacements:
            folder_name = folder_name.strip().replace(replacement, "")

        return folder_name

    def _is_valid_image_link(self, link):
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        for ext in valid_extensions:
            if link.endswith(ext):
                if self._is_image_corrupted(link):
                    return False
                return True
        return False

    @staticmethod
    def _is_image_corrupted(link):
        try:
            with requests.get(link) as r:
                if int(r.headers['Content-length']) <= 0:
                    logging.log(logging.ERROR, rf"Corrupted image found at: {link}")
                    return True

            return False
        except (IOError, SyntaxError) as e:
            logging.log(logging.ERROR, rf"Corrupted image found at: {link} - {e}")
            return True

    def _find_next_url(self, soup: BeautifulSoup, class_name: str) -> str | None:
        a_tag = soup.find('a', class_=class_name)
        if a_tag:
            url = a_tag['href'] if 'Next' in a_tag.get_text() else "None"
            if url.startswith("http"):
                return url

        return None

    def __str__(self):
        return self.name
