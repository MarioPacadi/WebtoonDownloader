import logging

from bs4 import BeautifulSoup
from Models.WebtoonDownloader import WebtoonsDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ReaperScans(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # <div class="flex flex-col justify-center items-center"></div>
            # //*[@id="content"]/div[1]
            div_element = soup.find('div', xPath='//*[@id="content"]/div[1]')
            if div_element is None:
                raise Exception(f"Required div element not found in the HTML. {div_element}")
            image_links = [img['src'] for img in div_element.find_all('img')]

            folder_name = self.get_folder_name(soup)

            next_url = None
            for a_tag in soup.find_all('a'):
                if 'Next' in a_tag.get_text():
                    next_url = a_tag['href']
                    break
            return image_links, next_url, folder_name
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None, None, None

    def get_folder_name(self, soup):
        # <h1 class="font-semibold font-sans text-foreground text-xs">Chapter 115</h1>
        folder_element = soup.find('h1', class_='font-semibold font-sans text-foreground text-xs')
        default_folder_name = f"Chapter{str(self.current_chapter).zfill(2)}"
        folder_name = folder_element.get_text().strip() if folder_element else default_folder_name
        folder_name = folder_name.replace(".", "")  # Remove any periods from the folder name
        return folder_name


if __name__ == '__main__':
    downloader = ReaperScans(
        starting_url="https://reaperscans.com/series/sss-class-suicide-hunter/chapter-115",
        folder_path="D:/Webtoons/SSS-Class Suicide Hunter")  # Replace with actual URL
    downloader.start_downloading()
