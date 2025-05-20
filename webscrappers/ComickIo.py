import logging

from bs4 import BeautifulSoup
from Models.WebtoonDownloader import WebtoonsDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ComickIo(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            div_element = soup.find('div', id='images-reader-container')
            if div_element is None:
                raise Exception(f"Required div element not found in the HTML. {div_element}")
            image_links = [img['src'] for img in div_element.find_all('img')]

            folder_name = self.get_folder_name(soup)

            base_url = "https://comick.io/"
            next_url = None
            # Find all <a> elements with the specified class (partial match or full)
            a_elements = soup.find_all('a', class_="w-12 hover:bg-gray-200 dark:hover:bg-gray-600 h-10 flex items-center shrink-0")
            for a in a_elements:
                svg = a.find('svg', class_='pl-1')
                if svg:
                    next_url = a['href']
                    if not next_url.startswith('http'):
                        next_url = base_url + next_url
                        
            return image_links, next_url, folder_name
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None, None, None

    def get_folder_name(self, soup):
        selected_option = soup.find('option', selected=True)
        if selected_option:
            folder_name = self.check_and_return_value(selected_option.text.strip())
        else:
            default_folder_name = f"Chapter{str(self.current_chapter).zfill(2)}"
            folder_name = default_folder_name
            print("No selected option found.")
            
        return folder_name
        
    def check_and_return_value(text):
        # Remove whitespace if any
        if text.isdigit():
            # Text contains only digits (numbers)
            return text  # or int(text) if you want integer
        elif text.isalpha():
            # Text contains only letters
            return None  # or any other indication you want
        else:
            # Text contains mixed characters or other symbols
            return None


if __name__ == '__main__':
    downloader = ComickIo(
        starting_url="https://comick.io/comic/02-sss-class-suicide-hunter/gSX6NoCx-chapter-116-en",
        folder_path="D:\Stripovi\SSS-Class Suicide Hunter")  # Replace with actual URL
    downloader.start_downloading()
