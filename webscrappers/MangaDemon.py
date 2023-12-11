import os
from io import BytesIO
from typing import List

import requests
from PIL import Image
from bs4 import BeautifulSoup
import logging

from Models.WebtoonDownloader import WebtoonsDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MangaDemon(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Finding the folder name from the h2 text within the div with class "titles"
            folder_element = soup.find('div', class_='titles').find('h2')
            folder_name = self._clean_folder_name(folder_element.get_text())

            # Extracting image links from the div with style attribute "overflow-x:hidden;max-width: 100%;"
            section_el = soup.find('section', class_='page-in content-wrap')
            if section_el:
                image_links = [img['src'] for img in section_el.find_all('img') if
                               self._is_valid_image_link(img.get('src'))]
            else:
                image_links = []

            # Adding the base URL to the incomplete next_url
            base_url = "https://manga-demon.org"
            next_url = None
            for a_tag in soup.find_all('a', class_='nextchap'):
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
    downloader = MangaDemon(
        "https://manga-demon.org/manga/Survival-Story-of-a-Sword-King-in-a-Fantasy-World/chapter/0-VA41", "Survival Story Of A Sword King In A Fantasy World")
    downloader.current_chapter = 0
    downloader.start_downloading()
