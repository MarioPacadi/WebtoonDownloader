import io
import logging
import os

import requests
from PIL import Image


# https://v18.mkklcdnv6tempv5.com/img/tab_18/03/42/51/iz985608/chapter_100_what_remains_unchanging_2/5-o.jpg


def download_images(image_links, parent_folder, folder_name):
    if not image_links:
        logging.warning("No images found for this chapter.")
        return

    for idx, link in enumerate(image_links):
        image_name = f"{folder_name} - image{idx + 1}.jpg"
        file_path = os.path.join(parent_folder, folder_name, image_name)

        if os.path.exists(file_path):
            logging.info(f"Image {image_name} already exists. Skipping download.")
            continue

        with requests.get(link) as r:
            if r.status_code == 200:
                with io.BytesIO(r.content) as f:
                    try:
                        img = Image.open(f)
                        img.convert("RGB").save(file_path, "JPEG")
                        logging.info(rf"Downloaded {link} to {file_path}")
                    except Exception as e:
                        print(f"Failed to convert image: {e}")
            else:
                print(f"Failed to download image {image_name}.")


image_links = [
    "https://v18.mkklcdnv6tempv5.com/img/tab_18/03/42/51/iz985608/chapter_100_what_remains_unchanging_2/5-o.jpg"]
folder_name = "TestImages"
parent_folder = "Default_Folder_Name"

os.makedirs(os.path.join(parent_folder, folder_name), exist_ok=True)
download_images(image_links, parent_folder, folder_name)
