import os
import sys

import customtkinter as ctk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.weather_service import fetch_weather


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WeatherApp:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title("Weather App")
        self.root.geometry("600x500")

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):

        # Title
        self.title_label = ctk.CTkLabel(
            self.root,
            text="🌤 Weather App",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=20)

        # Search Frame
        self.search_frame = ctk.CTkFrame(self.root)
        self.search_frame.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # City Entry
        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Enter city name"
        )
        self.city_entry.pack(
            side="left",
            padx=10,
            pady=10,
            fill="x",
            expand=True
        )

        # Search Button
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            command=self.on_search
        )
        self.search_button.pack(
            side="right",
            padx=10,
            pady=10
        )

        # Bind Enter key to search
        self.city_entry.bind("<Return>", lambda e: self.on_search())

        # Weather Card
        self.weather_frame = ctk.CTkFrame(self.root)
        self.weather_frame.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        # City
        self.city_label = ctk.CTkLabel(
            self.weather_frame,
            text="City: -",
            font=("Arial", 18, "bold")
        )
        self.city_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # Temperature
        self.temp_label = ctk.CTkLabel(
            self.weather_frame,
            text="Temperature: - °C",
            font=("Arial", 16)
        )
        self.temp_label.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        # Weather
        self.weather_label = ctk.CTkLabel(
            self.weather_frame,
            text="Weather: -",
            font=("Arial", 16)
        )
        self.weather_label.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        # Humidity
        self.humidity_label = ctk.CTkLabel(
            self.weather_frame,
            text="Humidity: - %",
            font=("Arial", 16)
        )
        self.humidity_label.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        # Wind Speed
        self.wind_label = ctk.CTkLabel(
            self.weather_frame,
            text="Wind Speed: - m/s",
            font=("Arial", 16)
        )
        self.wind_label.pack(
            anchor="w",
            padx=20,
            pady=5
        )

    def on_search(self):
        city = self.city_entry.get().strip()
        if not city:
            self.city_label.configure(text="City: Please enter a city name")
            return

        # Disable button during fetch
        self.search_button.configure(state="disabled")
        self.root.update()

        try:
            data = fetch_weather(city)

            if "error" in data:
                self.city_label.configure(text=f"Error: {data.get('error')}")
                self.temp_label.configure(text="Temperature: -")
                self.weather_label.configure(text="Weather: -")
                self.humidity_label.configure(text="Humidity: -")
                self.wind_label.configure(text="Wind Speed: -")
                return

            # Extract data
            city_name = data.get("name", "-")
            temperature = data.get("main", {}).get("temp", "-")
            weather = data.get("weather", [{}])[0].get("main", "-")
            humidity = data.get("main", {}).get("humidity", "-")
            wind_speed = data.get("wind", {}).get("speed", "-")

            # Update labels
            self.city_label.configure(text=f"City: {city_name}")
            self.temp_label.configure(text=f"Temperature: {temperature} °C")
            self.weather_label.configure(text=f"Weather: {weather}")
            self.humidity_label.configure(text=f"Humidity: {humidity} %")
            self.wind_label.configure(text=f"Wind Speed: {wind_speed} m/s")

        except Exception as e:
            self.city_label.configure(text=f"Error: {str(e)}")
        finally:
            self.search_button.configure(state="normal")


if __name__ == "__main__":
    app = WeatherApp()