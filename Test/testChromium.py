import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _download_html(url):
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
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    # Wait for all images to load before getting the page source
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
    time.sleep(2)  # Wait for 2 seconds to ensure all images are loaded
    html_content = driver.page_source
    driver.quit()
    return html_content


html = _download_html(
    "https://asuratoon.com/8223257861-the-greatest-estate-developer-chapter-105/")
print(html)
