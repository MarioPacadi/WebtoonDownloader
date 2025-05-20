import gdown
from bs4 import BeautifulSoup

import urllib.parse

from Models.CustomLogging import CustomLogging
from Models.WebtoonDownloader import WebtoonsDownloader

import requests
import time
import logging

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'

def get_html_from_url(url, max_retries=3, backoff_factor=0.5):
    """Fetches HTML content from a URL with retries and exponential backoff.

    Args:
        url (str): The URL to fetch.
        max_retries (int, optional): Maximum number of retries. Defaults to 3.
        backoff_factor (float, optional): Factor for increasing the delay between retries. Defaults to 0.5.

    Returns:
        str: The HTML content if successful, otherwise None.
    """

    retries = 0
    while retries < max_retries:
        try:
            headers = {
                'user-agent': user_agent}
            r = requests.get(url,headers=headers)
            r.raise_for_status()  # Raise an exception for bad status codes
            logging.info(f"Successfully fetched HTML from {url}")
            return r.text
        except requests.exceptions.ConnectionError as e:
            logging.warning(f"Connection error while fetching {url}: {e}. Retrying...")
            retries += 1
            backoff = backoff_factor ** retries
            time.sleep(backoff)  # Exponential backoff
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred while fetching {url}: {e}")
            return None

    logging.error(f"Failed to fetch HTML from {url} after {max_retries} retries.")
    return None


def download_file_from_google_drive(url, parent_folder):
    # Downloads a file from a Google Drive link.
    try:
        gdown.download(url, output=parent_folder, quiet=False, fuzzy=True, user_agent=user_agent)
    except Exception as e:
        print(f"Error downloading file: {e}")


class ZabavaBalkan(WebtoonsDownloader):

    # def _recursive_page_traversal(self, url, image_links):
    #     """Recursively traverses pages and extracts PDF URLs."""
    #
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #
    #     # Find the strip menu element
    #     strip_menu_element = soup.find('section', class_='strip__menu')
    #     if strip_menu_element:
    #         for menu_element in strip_menu_element.find_all('a', href=True):
    #             strip_url = urllib.parse.urljoin("https://zabavabalkan.website/", menu_element['href'])
    #
    #             # Recursively call the function for each menu link
    #             self._recursive_page_traversal(strip_url, image_links)
    #
    #     iframe = soup.find('iframe')
    #     if iframe:
    #         google_drive_pdf_url = iframe['src']
    #         image_links.append(google_drive_pdf_url)

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # folder_name = f"Chapter {str(self.current_chapter).zfill(2)}"
            folder_element = soup.find('section', class_='top__text').find('h2')
            if folder_element:
                chap = folder_element.get_text().strip().replace(f"{self.name} ", "")
                folder_name = self._clean_folder_name(chap)
            else:
                folder_name = f"Alan Ford"
            print(folder_element)

            # <div class="py-8 -mx-5 md:mx-0 flex flex-col items-center justify-center">/div>
            div_el = soup.find('section', class_='navigate__pages')
            if div_el:
                image_links = []
                # <img src=".webp" class="object-cover mx-auto" alt="chapter page">
                # for page in div_el.find_all('a', href=True):
                #     default_url = urllib.parse.urljoin("https://zabavabalkan.website/", page['href'])
                #     self._recursive_page_traversal(default_url, image_links)
                # print(div_el)
                for page in div_el.find_all('a', href=True):
                    default_url = urllib.parse.urljoin("https://zabavabalkan.website/", page['href'])
                    print(default_url)
                    page_html = get_html_from_url(default_url)
                    if page_html:
                        page_html_soup = BeautifulSoup(page_html, 'html.parser')
                        strip_menu_element = page_html_soup.find('section', class_='strip__menu').find_all('a',
                                                                                                           href=True)
                        for menu_element in strip_menu_element:
                            strip_url = urllib.parse.urljoin("https://zabavabalkan.website/", menu_element['href'])
                            strip_html = get_html_from_url(strip_url)
                            if strip_html:
                                strip_html_soup = BeautifulSoup(strip_html, 'html.parser')
                                iframe = strip_html_soup.find('iframe')
                                google_drive_pdf_url = iframe['src']
                                image_links.append(google_drive_pdf_url)
                                logging.log(CustomLogging.INSIGHT.value, f"Got google driver file link: {google_drive_pdf_url}")
                            else:
                                logging.log(logging.ERROR,
                                            f"FAILED TO GET HTML FROM: {strip_url}")
            else:
                image_links = []

            next_url = ""
            print(image_links)

            return image_links, next_url, folder_name
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None, None, None

    @staticmethod
    def _download_images(image_links, parent_folder, folder_name):
        if not image_links:
            logging.log(logging.WARNING, "No links found.")
            return

        for drive_file in image_links:
            url = str(drive_file).replace("/preview", "/view")
            download_file_from_google_drive(url, "D:\\Stripovi\\AlanFord\\")
            logging.log(CustomLogging.SHOWCASE.value, f"Downloaded file {url}")
