import os

import customtkinter
from PIL import Image

from view.utils.CropToCircle import crop_to_circle

import customtkinter as ctk
import tkinter as tk


class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = tk.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = ctk.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = ctk.CTkButton(self, text="Command", width=100, height=24)
        if self.command is not None:
            self._bind_label_click(label, item)
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return

    def remove_all(self):
        for label, button in zip(self.label_list, self.button_list):
            label.destroy()
            button.destroy()
            self.label_list.remove(label)
            self.button_list.remove(button)

    def _bind_label_click(self, label, item):
        label.bind("<Button-1>", lambda event: self.command(item))


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CTkScrollableFrame example")
        self.grid_rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=300,
                                                                        command=self.label_button_frame_event,
                                                                        corner_radius=0)
        self.scrollable_label_button_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

        logo = crop_to_circle("/assets/ReaperScans.png")

        for i in range(20):  # add items with images
            self.scrollable_label_button_frame.add_item(f"image and item {i}", image=customtkinter.CTkImage(
                logo,
                size=(64, 64)))
            # Image.open(os.path.join(current_dir, "assets", "BookwormLogo.png"))))

    @staticmethod
    def label_button_frame_event(item):
        print(f"label button frame clicked: {item}")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
