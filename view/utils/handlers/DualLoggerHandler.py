import logging
import re

import customtkinter as ctk
import darkdetect

from Models.CustomLogging import CustomLogging

# logging.basicConfig(level=CustomLogging.TRACE.value, format='%(asctime)s - %(levelname)s - %(message)s')


class DualLoggerHandler(logging.Handler):

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text: ctk.CTkTextbox = text

        # default_text_color: str = "white" if darkdetect.isDark() else "black"

        # Create tags for different log levels
        CustomLogging.add_tags_to_widget(self.text)
        logging.basicConfig(level=CustomLogging.TRACE.value, format='%(asctime)s - %(levelname)s - %(message)s')

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            # self.text.insert(ctk.END, msg + '\n', tags=record.levelname)
            self.insert_with_highlighted_urls(self.text, msg, record.levelname)
            # Autoscroll to the bottom
            self.text.yview(ctk.END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

    @staticmethod
    def insert_with_highlighted_urls(text_widget, message, default_tag):
        # Define a regular expression to match URLs and file paths
        url_pattern = r'(https?://[^"]+)'
        file_path_pattern = r'[A-Za-z]:/.*\.[A-Za-z]+'

        # Split the message into parts by the quote symbol
        # Replace single quotes with double quotes and then split
        modified_string = message.replace("'", '"')
        parts = modified_string.split('"')

        # parts = re.split("\"", message)
        for part in parts:
            content = part
            if re.match(url_pattern, content) or re.match(file_path_pattern, content):
                # Use a different tag for URLs and file paths
                text_widget.insert(ctk.END, content, tags=CustomLogging.INSIGHT.name)
            else:
                # Use the provided tag_name for other text
                text_widget.insert(ctk.END, content, tags=default_tag)

        text_widget.insert(ctk.END, '\n', tags=default_tag)
