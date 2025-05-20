import time

from bs4 import BeautifulSoup
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Models.WebtoonDownloader import WebtoonsDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MangaRead(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Finding the folder name
            folder_element = soup.find('div', class_='wp-manga-nav').find('li', class_="active")
            folder_name = self._clean_folder_name(folder_element.get_text())

            # Extracting image links
            images_el = soup.find_all('img',
                                      class_="wp-manga-chapter-img img-responsive effect-fade lazyloaded")
            if images_el:
                image_links = [img['src'] for img in images_el
                               if self._is_valid_image_link(img.get('src'))]
            else:
                image_links = []

            # Adding the base URL to the incomplete next_url
            base_url = "https://www.mangaread.org"
            next_url = None
            for a_tag in soup.find_all('a', class_='btn next_page'):
                url = str(a_tag.get('href', ''))
                if url.startswith("http"):
                    next_url = url
                else:
                    next_url = base_url + url
                break

            if folder_name and image_links:
                return image_links, next_url, folder_name
            else:
                raise Exception("Error parsing folder name or image links.")
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return [], None, "Default_Folder_Name"


if __name__ == '__main__':
    downloader = MangaRead(
        "https://www.mangaread.org/manga/survival-story-of-a-sword-king-in-a-fantasy-world-manhua/chapter-1/",
        "Survival Story Of A Sword King In A Fantasy World")
    downloader.current_chapter = 1
    downloader.start_downloading()
