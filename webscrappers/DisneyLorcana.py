import json
import time

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from Models.WebtoonDownloader import WebtoonsDownloader

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class DisneyLorcana(WebtoonsDownloader):

    def _execute_user_simulated_interaction(self, driver: WebDriver):
        all_dropdown = driver.find_elements(By.CLASS_NAME, "dropdown-toggle")
        all_dropdown[0].click()
        # checkboxes = all_dropdown[0].find_elements(By.XPATH, "//input[@type='checkbox']")
        # for checkbox in checkboxes:
        #     checkbox.click()

        # Wait for all images to load before getting the page source
        WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
        time.sleep(15)  # Wait for 2 seconds to ensure all images are loaded
        print("Executing user simulated interaction")

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            print("Starting parsing html")
            folder_name = f"Disney Lorcana"

            div_el = soup.find('div',
                               class_='max-w-7xl items-center mx-auto grid grid-cols-2 '
                                      'gap-1 sm:grid-cols-3 sm:gap-2 md:grid-cols-4 md:gap-4 px-8 py-4')
            # div_el=soup.find("div", xPath_='//*[@id="app"]/div/div[2]/main/div[4]/div/div[1]')

            if div_el is None:
                print("Div holder of links not found")

            if div_el:
                # <img data-v-ffa61567="" onclick="cardModal.showModal()" alt="gallery"
                # src="https://images.lorcania.com/cards/p2/14_en_scar-716.webp" loading="lazy"
                # class="w-full h-full border rounded-[3%] border-gray-700 bg-gray-700
                # hover:drop-shadow-lg hover:border-blue-600 hover:bg-indigio-80">
                img_els = div_el.find_all(name='img',
                                          class_='w-full h-full border rounded-[3%] border-gray-700 bg-gray-700 '
                                                 'hover:drop-shadow-lg hover:border-blue-600 hover:bg-indigio-80')
                print("Processing image links")
                # image_links = [img['src'] for img in img_els if
                #                'src' in img.attrs and self._is_valid_image_link(img['src'])]
                image_links = []
                for img in img_els:
                    if 'src' in img.attrs and self._is_valid_image_link(img['src']):
                        print(f"Processing image link ({img_els.index(img)})")
                        image_links.append(img['src'])
            else:
                image_links = []

            if not image_links:
                print("No images found")

            next_url = None

            return image_links, next_url, folder_name
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None, None, None
