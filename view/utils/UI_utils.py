import customtkinter as ctk


def change_text_widget_data(text_widget, text: str):
    text_widget.delete(0, ctk.END)  # Uncomment if you need to replace text instead of adding
    text_widget.insert(ctk.END, text)
