import logging
import threading
import time

import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Models.LoadingBar import start_loading, done_loading


def _download_html(url):
    start_loading("Downloading HTML")
    driver_path = "D:/Program Files (x86)/chromedriver-win64/chromedriver.exe"
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

    options = Options()
    options.binary_location = brave_path
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--incognito")  # Run Chrome in incognito mode
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Brave/9085")  # Add user-agent to the options
    chrome_driver_path = driver_path  # Replace with the actual path to chromedriver
    service = Service(chrome_driver_path)
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(url)
        # Wait for all images to load before getting the page source
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
        time.sleep(2)  # Wait for 2 seconds to ensure all images are loaded
        html_content = driver.page_source
    done_loading()
    return html_content


def _parse_html(html_content):
    try:
        start = time.time()
        start_loading("Parsing HTML", 730)
        soup = BeautifulSoup(html_content, 'html.parser')

        folder_element = soup.find('div', class_='headpost').find('h1')
        if folder_element:
            chap = folder_element.get_text().strip().replace("Omniscient Reader’s Viewpoint ", "")
            folder_name = _clean_folder_name(chap)

        div_el = soup.find('div', class_='rdminimal')
        if div_el:
            # img_els = div_el.find_all(name='img', class_='ts-main-image')
            img_els = div_el.find_all(name='img')
            image_links = [img['src'] for img in img_els if
                           _is_valid_image_link(img.get('src'))]
        else:
            image_links = []

        next_url = None
        a_tag = soup.find('a', class_="ch-next-btn")
        if a_tag:
            if 'Next' in a_tag.get_text():
                next_url = a_tag['href']

        done_loading()
        end = time.time()
        print(f"Length in seconds: {end - start}")
        return image_links, next_url, folder_name
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return None, None, None


def _clean_folder_name(folder_name):
    # Folders must not use symbols \/:*?"<>|
    folder_name = folder_name.strip().replace(":", " -")
    replacements = ['\\', "/", "*", "?", "<", ">", "|"]
    for replacement in replacements:
        folder_name = folder_name.strip().replace(replacement, "")

    return folder_name


def _is_valid_image_link(link):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    for ext in valid_extensions:
        if link.endswith(ext):
            if _is_image_corrupted(link):
                return False
            return True
    return False


def _is_image_corrupted(link):
    try:
        with requests.get(link) as r:
            if int(r.headers['Content-length']) <= 0:
                print(rf"Corrupted image found at: {link}")
                return True

        return False
    except (IOError, SyntaxError) as e:
        print(rf"Corrupted image found at: {link} - {e}")
        return True


html = _download_html("https://flamecomics.com/omniscient-readers-viewpoint-chapter-27/")
image_links, next_url, folder_name = _parse_html(html)
