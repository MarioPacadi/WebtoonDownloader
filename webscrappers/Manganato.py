from bs4 import BeautifulSoup
import logging

from Models.WebtoonDownloader import WebtoonsDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Manganato(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Finding the last element with the class "a-h" in the div with class "panel-breadcrumb"
            folder_element = soup.find('div', class_='panel-breadcrumb').find_all('a', class_='a-h')[-1]
            folder_name = self._clean_folder_name(folder_element.get_text())

            # Extracting image links from the div with the class "container-chapter-reader"
            div_element = soup.find('div', class_='container-chapter-reader')
            image_links = [img['src'] for img in div_element.find_all('img') if self._is_valid_image_link(img['src'])]
            print(image_links)
            next_url = None
            for a_tag in soup.find_all('a', class_='navi-change-chapter-btn-next'):
                if 'NEXT CHAPTER' in a_tag.get_text():
                    next_url = a_tag['href']
                    break

            return image_links, next_url, folder_name
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None, None, None

    @staticmethod
    def _clean_folder_name(folder_name):
        # folder_name = folder_name.strip().replace(" ", "_")
        folder_name = folder_name.replace(":", " -")
        return folder_name

    @staticmethod
    def _is_valid_image_link(link):
        valid_extensions = ['.jpg', '.jpeg', '.png']
        for ext in valid_extensions:
            if link.endswith(ext):
                return True
        return False

    @staticmethod
    def _is_advertisement(img_tag):
        # Check if the img_tag belongs to an advertisement
        parent_classes = img_tag.parent.get('class', [])
        return 'bg-ssp' in parent_classes or 'bg-im' in parent_classes


if __name__ == '__main__':
    downloader = Manganato(
        "https://chapmanganato.com/manga-iz985608/chapter-0", "Omniscient Readers Viewpoint")
    downloader.start_downloading()
