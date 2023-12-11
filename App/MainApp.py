import json
import logging
import threading

import customtkinter as ctk
from customtkinter import CTk

from Models import WebtoonDownloader
from Models.CustomLogging import CustomLogging
from Models.WebtoonScrapper import scrapper_directory_path, get_icon_by_scrapper_name
from repo import WebtoonDB
from repo.WebtoonDB import add_data_to_json_file, update_data_of_json_file
from view.components.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame
from view.components.WebtoonForm import WebtoonForm
from view.utils import FileManager
from view.utils.CropToCircle import crop_to_circle
from view.utils.FileManager import import_classes_from_directory_of_subclass_webtoons_downloader
from view.utils.WebtoonEncoder import WebtoonEncoder
from view.utils.handlers.DualLoggerHandler import DualLoggerHandler


def download_webtoon(webtoon: WebtoonDownloader):
    background_thread = threading.Thread(target=webtoon.start_downloading, args=[])
    background_thread.start()


class MyApp(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Webtoon Downloader")

        # First row
        label_webtoon_list = ctk.CTkLabel(self, text="Webtoon list", font=("Helvetica", 16, "bold"))
        label_webtoon_list.grid(row=0, column=0, sticky="n", pady=10, padx=10)

        self.frame_row1_col1 = ScrollableLabelButtonFrame(self, width=300, command=self.label_button_frame_event,
                                                          corner_radius=0)
        self.frame_row1_col1.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.frame_row1_col2 = WebtoonForm(self,
                                           add_command=self.perform_add,
                                           update_command=self.perform_update,
                                           download_command=self.perform_download
                                           )
        self.frame_row1_col2.grid(row=1, column=1, sticky="nsew", pady=(0, 10), padx=10)

        # Second row
        label_logs = ctk.CTkLabel(self, text="Logs", font=("Helvetica", 16, "bold"))
        label_logs.grid(row=2, column=0, columnspan=2, sticky="n", pady=10)

        self.frame_row2 = ctk.CTkFrame(self)
        self.frame_row2.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10, padx=10)

        # Configure row and column weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Widgets for the first row, column 1 (Scrollable Frame)
        self.fill_scrollable_frame()

        # Widgets for the first row, column 1 (WebtoonForm)

        # Widgets for the second row (Logs window)
        logs_text = ctk.CTkTextbox(self.frame_row2, wrap="word", height=10, width=80, state='disabled', pady=10, padx=10)
        logs_text.grid(row=0, column=0, sticky="nsew")

        # Set up logging
        # Create textLogger
        text_handler = DualLoggerHandler(logs_text)

        # Logging configuration
        logging.basicConfig(filename='test.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)

        # Configure row and column weights for resizing
        self.frame_row1_col2.grid_columnconfigure(1, weight=1)
        # self.frame_row1_col2.grid_rowconfigure(0, weight=1)   # This was the problem
        self.frame_row2.grid_rowconfigure(0, weight=1)
        self.frame_row2.grid_columnconfigure(0, weight=1)

        # Set minimum height for logs text
        self.frame_row2.grid_rowconfigure(0, minsize=300)

        # Schedule the fullscreen setting after a delay (10 milliseconds in this example)
        self.after(10, self.set_fullscreen)

    def set_fullscreen(self):
        self.state('zoomed')

    def label_button_frame_event(self, item):
        logging.info(f"{item}\n")
        self.frame_row1_col2.set_data(item)

    def fill_scrollable_frame(self):
        # all_class_instances = import_classes_from_directory_of_subclass_webtoons_downloader(scrapper_directory_path)
        self.frame_row1_col1.remove_all()
        webtoon_list = WebtoonDB.read_data_from_json_file(filename=WebtoonDB.json_db_path)
        for webtoon in webtoon_list:  # add items with images
            scrapper_name = webtoon.__class__.__name__
            logo = crop_to_circle(get_icon_by_scrapper_name(scrapper_name))
            self.frame_row1_col1.add_item(webtoon, image=ctk.CTkImage(
                logo,
                size=(64, 64)))

    # Button Actions
    def perform_add(self):
        # Get data from entries and perform "Add" action
        webtoon = self.frame_row1_col2.get_data()
        logging.warning(f"Performing 'Add' action with data: {webtoon}\n")
        json_str = webtoon.to_json()
        logging.warning(json_str)
        add_data_to_json_file(data=[webtoon], filename=WebtoonDB.json_db_path)
        self.fill_scrollable_frame()

    def perform_download(self):
        # Get data from entries and perform "Download" action
        webtoon = self.frame_row1_col2.get_data()
        print_str = f"Performing 'Download' action with data: {webtoon}\n"
        logging.warning(print_str)
        download_webtoon(webtoon)

    def perform_update(self):
        # Get data from entries and perform "Update" action
        webtoon = self.frame_row1_col2.get_data()
        print_str = f"Performing 'Update' action with data: {webtoon}\n"
        logging.info(print_str)
        update_data_of_json_file(update_target=webtoon, filename=WebtoonDB.json_db_path)
        self.fill_scrollable_frame()


if __name__ == "__main__":
    CustomLogging.add_custom_levels()
    app = MyApp()
    app.mainloop()
