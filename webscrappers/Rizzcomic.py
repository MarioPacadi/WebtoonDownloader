from bs4 import BeautifulSoup
import logging
import re

from Models.CustomLogging import CustomLogging
from Models.LoadingBar import done_loading, start_loading
from Models.WebtoonDownloader import WebtoonsDownloader


class Rizzcomic(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            thread = start_loading("Parsing HTML", 730)
            soup = BeautifulSoup(html_content, 'html.parser')

            folder_element = soup.find('h1', class_='entry-title')
            if folder_element:
                chap = folder_element.get_text().strip()
                chap = self._clean_folder_name(chap)
                folder_name = self.clean_string(chap)

                print(folder_name)
            else:
                folder_name = f"Chapter{str(self.current_chapter).zfill(2)}"

            # id="readerarea" class="rdminimal"
            div_el = soup.find('div', class_='rdminimal')
            if div_el:
                # img_els = div_el.find_all(name='img', class_='ts-main-image')
                img_els = div_el.find_all(name='img')
                image_links = [img['src'] for img in img_els if
                               'src' in img.attrs and self._is_valid_image_link(img['src'])]
            else:
                image_links = []

            next_url = None
            a_tag = soup.find('a', class_="ch-next-btn")
            if a_tag:
                url = a_tag['href'] if 'Next' in a_tag.get_text() else "None"
                if url.startswith("http"):
                    next_url = url

            done_loading()
            if thread.is_alive():
                thread.join()

            return image_links, next_url, folder_name
        except Exception as e:
            done_loading()
            print(f"An error occurred during parsing: {e}")
            return None, None, None

    @staticmethod
    def clean_string(input_string):
        pattern = r'Chapter \d+'
        match = re.search(pattern, input_string)
        if match:
            return match.group()
        else:
            return input_string
