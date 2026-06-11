import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WeatherApp:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title("Weather App")

        self.root.geometry("600x500")

        self.root.mainloop()