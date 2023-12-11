import logging
import re

from Models.CustomLogging import CustomLogging
import customtkinter as ctk

from Test.testLoggerScreen import TextHandler
from view.utils.handlers.DualLoggerHandler import DualLoggerHandler

class SimpleUI(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("SimpleUI")

        self.frame_row1 = ctk.CTkFrame(self)
        self.frame_row1.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)

        logs_text = ctk.CTkTextbox(self.frame_row1, wrap="word", height=10, width=80, state='disabled', pady=10, padx=10)
        logs_text.grid(row=0, column=0, sticky="nsew")

        text_handler = DualLoggerHandler(logs_text)

        # Logging configuration
        logging.basicConfig(filename='test.log',
                            level=CustomLogging.TRACE.value,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)

        msg = "Downloaded \"https://media.reapercomics.com/file/4SRBHm/comics/b94680f2-7102-4e80-aba8-bf5ed93073cc/chapters/06ad2bb7-86dd-41e7-9b71-821eebf72cb0/000 NEW.png\" to \'D:/Webtoons/SSS-Class Suicide Hunter/Chapter 105/Chapter 105 - image1.jpg\'"
        download_button = ctk.CTkButton(self, text="Download", command=logging.log(CustomLogging.SHOWCASE.value, msg))
        download_button.grid(row=0, column=1, padx=5, pady=10)

        # Configure row and column weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configure row and column weights for resizing
        self.frame_row1.grid_rowconfigure(0, weight=1)
        self.frame_row1.grid_columnconfigure(0, weight=1)
        self.frame_row1.grid_rowconfigure(0, minsize=300)


# Example usage
# Create a text widget (replace this with your actual text widget)
if __name__ == "__main__":
    CustomLogging.add_custom_levels()
    app = SimpleUI()
    app.mainloop()
