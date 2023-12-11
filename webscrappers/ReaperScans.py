import logging

from bs4 import BeautifulSoup
from Models.WebtoonDownloader import WebtoonsDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ReaperScans(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            div_element = soup.find('div', class_='mx-auto max-w-2xl mt-8 lg:max-w-7xl')
            if div_element is None:
                raise Exception(f"Required div element not found in the HTML. {div_element}")
            image_links = [img['src'] for img in div_element.find_all('img')]

            folder_element = soup.find('div', class_='hidden md:flex text-white mb-2')
            default_folder_name = f"Chapter{str(self.current_chapter).zfill(2)}"
            folder_name = folder_element.get_text().strip() if folder_element else default_folder_name
            folder_name = folder_name.replace(" ", " ")  # Replace any spaces with underscores
            folder_name = folder_name.replace(".", "")  # Remove any periods from the folder name

            next_url = None
            for a_tag in soup.find_all('a'):
                if 'Next' in a_tag.get_text():
                    next_url = a_tag['href']
                    break
            return image_links, next_url, folder_name
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None, None, None


if __name__ == '__main__':
    downloader = ReaperScans(
        "https://reapercomics.com/comics/5150-sss-class-suicide-hunter/chapters/14091450-chapter-105",
        "D:/Webtoons/SSS-Class Suicide Hunter")  # Replace with actual URL
    downloader.start_downloading()
