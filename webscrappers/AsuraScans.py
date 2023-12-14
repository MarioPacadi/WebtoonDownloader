from bs4 import BeautifulSoup
import logging

from Models.WebtoonDownloader import WebtoonsDownloader


class AsuraScans(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            folder_element = soup.find('div', class_='headpost').find('h1')
            if folder_element:
                chap = folder_element.get_text().strip().replace("The Greatest Estate Developer ", "")
                folder_name = self._clean_folder_name(chap)
            else:
                folder_name = f"Chapter{str(self.current_chapter).zfill(2)}"

            div_el = soup.find('div', class_='rdminimal')
            if div_el:
                img_els = div_el.find_all(name='img', class_='ts-main-image')
                # img_els = div_el.find_all(name='img', width='800')
                image_links = [img['src'] for img in img_els if
                               self._is_valid_image_link(img.get('src'))]
            else:
                image_links = []

            next_url = None
            a_tag = soup.find('a', class_="ch-next-btn")
            if a_tag:
                if 'Next' in a_tag.get_text():
                    next_url = a_tag['href']

            return image_links, next_url, folder_name
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None, None, None


if __name__ == '__main__':
    downloader = AsuraScans(
        starting_url="https://asuratoon.com/8223257861-the-greatest-estate-developer-chapter-105/", name="The Greatest Estate Developer")
    downloader.current_chapter = 105
    downloader.start_downloading()
