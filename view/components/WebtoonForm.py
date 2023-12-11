import logging
import os
import uuid
from uuid import UUID

import customtkinter as ctk
import darkdetect
from customtkinter import CTk, filedialog, CTkEntry, CTkComboBox, CTkBaseClass, CTkFrame

from Models.WebtoonDownloader import WebtoonsDownloader
from Models.WebtoonScrapper import get_all_webtoon_scrappers, get_webtoon_downloader
from view.utils.UI_utils import change_text_widget_data


class WebtoonForm(CTkFrame):

    def __init__(self, master, add_command, update_command, download_command, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        # Action functions
        self.perform_add = add_command
        self.perform_update = update_command
        self.perform_download = download_command

        # Form fields
        self.hidden_id = uuid.uuid4()
        self.tf_startingUrl = self.set_label_entry(row=0, text="Starting Url:", text_color="cyan")
        self.tf_webtoonName = self.set_label_entry(row=1, text="Webtoon name:")
        self.cb_webscrapper = self.set_dropdown(row=2, label_text="Webscraper:",
                                                dropdown_values=get_all_webtoon_scrappers())
        self.parent_directory = "D:\\Webtoons"
        self.set_select_directory(row=3, label_text="Select directory:\n (optional)", btn_text="Browse",
                                  command=self.select_directory)

        # Action buttons
        add_button = ctk.CTkButton(self, text="Add", command=self.perform_add,
                                   fg_color="green", hover_color="darkgreen")
        add_button.grid(row=4, column=0, padx=5, pady=10)

        download_button = ctk.CTkButton(self, text="Download", command=self.perform_download)
        download_button.grid(row=4, column=1, padx=5, pady=10)

        update_button = ctk.CTkButton(self, text="Update", command=self.perform_update,
                                      fg_color="orange", hover_color="darkorange")
        update_button.grid(row=4, column=2, padx=5, pady=10)

    def select_directory(self):
        file_path = filedialog.askdirectory(title="Select a folder")
        if file_path:
            self.parent_directory = file_path
            logging.warning(f"Selected File: {file_path}\n")
            print(f"Selected File: {file_path}\n")
            # self.logs_text.insert(ctk.END, f"Selected File: {file_path}\n")
            # self.logs_text.see(ctk.END)  # Scroll to the end of the text

    def set_label_entry(self, text, row, text_color="") -> CTkEntry:

        # if text_color not set, then use OS theme
        if not text_color:
            if darkdetect.isDark():
                text_color = "white"
            else:
                text_color = "black"

        label = ctk.CTkLabel(self, text=text)
        label.grid(row=row, column=0, pady=20, padx=(50, 20), sticky="e")
        text_field = CTkEntry(self, width=400, text_color=text_color)
        text_field.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        return text_field

    def set_dropdown(self, label_text, row, dropdown_values=None) -> CTkComboBox:
        if dropdown_values is None:
            dropdown_values = []
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, pady=20, padx=5, sticky="e")
        dropdown = CTkComboBox(self, values=dropdown_values)
        dropdown.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        return dropdown

    def set_select_directory(self, row, label_text, btn_text, command):
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, pady=20, padx=5, sticky="e")
        select_file_button = ctk.CTkButton(self, text=btn_text, command=command)
        select_file_button.grid(row=row, column=1, pady=5, padx=5, sticky="w")

    def get_data(self):
        return get_webtoon_downloader(
            id_webtoon=self.hidden_id,
            webscrapper=self.cb_webscrapper.get(),
            name=self.tf_webtoonName.get(),
            url=self.tf_startingUrl.get(),
            save_to=self.parent_directory
        )

    def set_data(self, item: WebtoonsDownloader):
        self.hidden_id = item.id_webtoon
        change_text_widget_data(self.tf_webtoonName, item.name)
        change_text_widget_data(self.tf_startingUrl, item.starting_url)
        self.parent_directory = item.folder_path
        self.cb_webscrapper.set(item.__class__.__name__)
