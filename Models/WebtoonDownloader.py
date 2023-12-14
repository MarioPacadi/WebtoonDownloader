import io
import json
import logging
import os
import time
import uuid
import requests

from abc import abstractmethod, ABC
from dataclasses import dataclass
from PIL import Image
from dataclasses_json import dataclass_json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Models.LoadingBar import start_loading, done_loading
from Models.CustomLogging import CustomLogging
from Models.Settings import Settings

# logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')



@dataclass_json
@dataclass
class WebtoonsDownloader(ABC):
    id_webtoon: uuid.UUID
    starting_url: str
    current_chapter: int
    folder_path: str
    name: str
    icon_path: str

    def __init__(self,
                 id_webtoon: uuid.UUID = uuid.uuid4(),
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
                os.makedirs(os.path.join(self.folder_path, folder_name), exist_ok=True)
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
    @staticmethod
    def _download_html(url):
        html_content = ""
        try:
            start_loading("Downloading HTML")
            with open("./repo/settings.json", 'r+', encoding='utf-8') as f:
                json_str = json.load(f)
            settings = Settings.from_json(json_str)

            options = Options()
            options.binary_location = settings.browser_path
            options.add_argument("--headless")  # Run Chrome in headless mode

            if settings.run_in_incognito:
                options.add_argument("--incognito")  # Run Chrome in incognito mode

            options.add_argument(
                f"--user-agent={settings.user_agent}")  # Add user-agent to the options
            chrome_driver_path = settings.driver_path  # Replace with the actual path to chromedriver
            service = Service(chrome_driver_path)
            with webdriver.Chrome(service=service, options=options) as driver:
                driver.get(url)
                # Wait for all images to load before getting the page source
                WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
                time.sleep(2)  # Wait for 2 seconds to ensure all images are loaded
                html_content = driver.page_source
            done_loading()
        except Exception as e:
            done_loading()
            logging.error(e)

        return html_content

    @abstractmethod
    def _parse_html(self, html_content):
        pass

    @staticmethod
    def _download_images(image_links, parent_folder, folder_name):
        if not image_links:
            logging.warning("No images found for this chapter.")
            return

        for idx, link in enumerate(image_links):
            image_name = f"{folder_name} - image{idx + 1}.jpg"
            file_path = os.path.join(parent_folder, folder_name, image_name)

            if os.path.exists(file_path):
                logging.warning(f"Image \"{image_name}\" already exists. Skipping download.")
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
                    logging.error(rf"Corrupted image found at: {link}")
                    return True

            return False
        except (IOError, SyntaxError) as e:
            logging.error(rf"Corrupted image found at: {link} - {e}")
            return True

    def __str__(self):
        return self.name
