from bs4 import BeautifulSoup
import logging
import re

from Models.CustomLogging import CustomLogging
from Models.LoadingBar import done_loading, start_loading
from Models.WebtoonDownloader import WebtoonsDownloader


class ManhwaFreak(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            thread = start_loading("Parsing HTML", 730)
            soup = BeautifulSoup(html_content, 'html.parser')

            folder_element = soup.find('h2', class_='entry-title')
            if folder_element:
                chap = folder_element.get_text().strip()
                chap = self.clean_string(chap)
                folder_name = self._clean_folder_name(chap)
            else:
                folder_name = f"Chapter{str(self.current_chapter).zfill(2)}"

            # id="readerarea" class="readerarea"
            div_el = soup.find('div', class_='readerarea')
            if div_el:
                # img_els = div_el.find_all(name='img', class_='ts-main-image')
                img_els = div_el.find_all(name='img')
                image_links = [img['src'] for img in img_els if
                               'src' in img.attrs and self._is_valid_image_link(img['src'])
                               and img['src'] != "https://manhwa-freak.org/wp-content/uploads/2023/12/00-3.jpg" and
                               img['src'] != "https://manhwa-freak.org/wp-content/uploads/2023/11/100.5-685x1024.jpg"
                               ]
            else:
                image_links = []

            next_url = self._find_next_url(soup, "ch-next-btn")

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




# if __name__ == '__main__':
#     downloader = FlameComics(
#         starting_url="https://flamecomics.com/hero-has-returned-chapter-3/", name="Hero has returned")
#     downloader.current_chapter = 3
#     downloader.start_downloading()
