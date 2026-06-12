import os
import sys
import threading
from typing import Dict, Any

import customtkinter as ctk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.weather_service import fetch_weather


ctk.set_appearance_mode("dark")


class WeatherApp:
    # Weather-based color themes
    WEATHER_THEMES = {
        "Clear": {"primary": "#FFD700", "secondary": "#FFA500", "accent": "#FF8C00", "bg": "#1a1a2e"},
        "Clouds": {"primary": "#B0C4DE", "secondary": "#778899", "accent": "#708090", "bg": "#1a1a2e"},
        "Rain": {"primary": "#4A90E2", "secondary": "#2E5C8A", "accent": "#1E3A5F", "bg": "#0f1419"},
        "Drizzle": {"primary": "#87CEEB", "secondary": "#4A90E2", "accent": "#2E5C8A", "bg": "#0f1419"},
        "Thunderstorm": {"primary": "#9370DB", "secondary": "#6A5ACD", "accent": "#4B0082", "bg": "#0a0a0f"},
        "Snow": {"primary": "#E0F6FF", "secondary": "#B0E0E6", "accent": "#87CEEB", "bg": "#1a1a2e"},
        "Mist": {"primary": "#A9A9A9", "secondary": "#808080", "accent": "#696969", "bg": "#0f1419"},
    }

    WEATHER_EMOJIS = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
    }

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Weather App")
        self.root.geometry("700x650")
        self.root.resizable(False, False)

        self.current_theme = None
        self.is_loading = False

        self.create_widgets()
        self.root.mainloop()

    def get_weather_theme(self, weather_type: str) -> Dict[str, str]:
        """Get theme colors based on weather type."""
        for key in self.WEATHER_THEMES:
            if key.lower() in weather_type.lower():
                return self.WEATHER_THEMES[key]
        return self.WEATHER_THEMES["Clouds"]

    def get_weather_emoji(self, weather_type: str) -> str:
        """Get emoji based on weather type."""
        for key in self.WEATHER_EMOJIS:
            if key.lower() in weather_type.lower():
                return self.WEATHER_EMOJIS[key]
        return "🌤️"

    def apply_theme(self, theme: Dict[str, str]):
        """Apply weather-based theme to the UI."""
        if theme == self.current_theme:
            return
        self.current_theme = theme
        self.root.configure(fg_color=theme["bg"])

    def create_widgets(self):
        """Create and layout all UI widgets."""
        # Main container with padding
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Header section
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🌍 Weather Forecast",
            font=("Helvetica", 32, "bold"),
            text_color="#FFFFFF"
        )
        self.title_label.pack(anchor="w")

        # Search section
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.pack(fill="x", padx=20, pady=10)

        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Enter city name...",
            font=("Helvetica", 14),
            height=45
        )
        self.city_entry.pack(side="left", padx=(0, 10), fill="both", expand=True)
        self.city_entry.bind("<Return>", lambda e: self.search_in_thread())

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            command=self.search_in_thread,
            font=("Helvetica", 14, "bold"),
            height=45,
            width=100
        )
        self.search_button.pack(side="right")

        # Weather display card
        self.weather_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.weather_card.pack(fill="both", expand=True, padx=20, pady=10)

        # Weather icon and temperature section
        self.temp_section = ctk.CTkFrame(self.weather_card, fg_color="transparent")
        self.temp_section.pack(fill="x", padx=30, pady=(30, 20))

        self.weather_icon = ctk.CTkLabel(
            self.temp_section,
            text="🌤️",
            font=("Arial", 80),
            text_color="#FFFFFF"
        )
        self.weather_icon.pack(side="left", padx=(0, 20))

        self.temp_display_frame = ctk.CTkFrame(self.temp_section, fg_color="transparent")
        self.temp_display_frame.pack(side="left", fill="both", expand=True)

        self.city_label = ctk.CTkLabel(
            self.temp_display_frame,
            text="--",
            font=("Helvetica", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.city_label.pack(anchor="w")

        self.temp_label = ctk.CTkLabel(
            self.temp_display_frame,
            text="-- °C",
            font=("Helvetica", 48, "bold"),
            text_color="#FFFFFF"
        )
        self.temp_label.pack(anchor="w")

        self.weather_label = ctk.CTkLabel(
            self.temp_display_frame,
            text="--",
            font=("Helvetica", 16),
            text_color="#CCCCCC"
        )
        self.weather_label.pack(anchor="w", pady=(5, 0))

        # Details section
        self.details_frame = ctk.CTkFrame(self.weather_card, fg_color="transparent")
        self.details_frame.pack(fill="x", padx=30, pady=(0, 30))

        # Create detail rows
        self.create_detail_row(self.details_frame, "💧 Humidity", "humidity_label", 0)
        self.create_detail_row(self.details_frame, "💨 Wind Speed", "wind_label", 1)
        self.create_detail_row(self.details_frame, "🌡️ Feels Like", "feels_like_label", 2)
        self.create_detail_row(self.details_frame, "👁️ Visibility", "visibility_label", 3)

        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready",
            font=("Helvetica", 11),
            text_color="#999999"
        )
        self.status_label.pack(pady=(0, 10))

    def create_detail_row(self, parent: ctk.CTkFrame, label_text: str, attr_name: str, row: int):
        """Create a detail row with label and value."""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)

        label = ctk.CTkLabel(
            row_frame,
            text=label_text,
            font=("Helvetica", 13),
            text_color="#AAAAAA",
            width=150
        )
        label.pack(side="left")

        value_label = ctk.CTkLabel(
            row_frame,
            text="--",
            font=("Helvetica", 13, "bold"),
            text_color="#FFFFFF"
        )
        value_label.pack(side="right")

        setattr(self, attr_name, value_label)

    def search_in_thread(self):
        """Search for weather in a background thread."""
        if self.is_loading:
            return

        city = self.city_entry.get().strip()
        if not city:
            self.status_label.configure(text="Please enter a city name")
            return

        self.is_loading = True
        self.search_button.configure(state="disabled")
        self.status_label.configure(text="Loading...")

        thread = threading.Thread(target=self.fetch_and_update, args=(city,), daemon=True)
        thread.start()

    def fetch_and_update(self, city: str):
        """Fetch weather data and update UI."""
        try:
            data = fetch_weather(city)

            if "error" in data:
                self.root.after(0, self.show_error, data.get("error", "Unknown error"))
                return

            self.root.after(0, self.update_ui, data)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            self.is_loading = False
            self.root.after(0, lambda: self.search_button.configure(state="normal"))

    def update_ui(self, data: Dict[str, Any]):
        """Update UI with weather data."""
        try:
            # Extract data
            city_name = data.get("name", "--")
            temperature = data.get("main", {}).get("temp", "--")
            weather = data.get("weather", [{}])[0].get("main", "--")
            humidity = data.get("main", {}).get("humidity", "--")
            wind_speed = data.get("wind", {}).get("speed", "--")
            feels_like = data.get("main", {}).get("feels_like", "--")
            visibility = data.get("visibility", "--")
            if visibility != "--":
                visibility = f"{int(visibility) / 1000:.1f} km"

            # Get theme and emoji
            theme = self.get_weather_theme(weather)
            emoji = self.get_weather_emoji(weather)

            # Apply theme
            self.apply_theme(theme)
            self.weather_card.configure(fg_color=theme["secondary"])

            # Update colors
            self.search_button.configure(fg_color=theme["primary"], text_color="#000000" if theme["primary"] in ["#FFD700", "#E0F6FF"] else "#FFFFFF")

            # Update labels
            self.weather_icon.configure(text=emoji)
            self.city_label.configure(text=city_name)
            self.temp_label.configure(text=f"{temperature}°" if temperature != "--" else "--")
            self.weather_label.configure(text=weather)
            self.humidity_label.configure(text=f"{humidity}%" if humidity != "--" else "--")
            self.wind_label.configure(text=f"{wind_speed} m/s" if wind_speed != "--" else "--")
            self.feels_like_label.configure(text=f"{feels_like}°C" if feels_like != "--" else "--")
            self.visibility_label.configure(text=str(visibility))

            self.status_label.configure(text="Weather updated")
        except Exception as e:
            self.show_error(f"UI Update Error: {str(e)}")

    def show_error(self, error_msg: str):
        """Display error message."""
        self.status_label.configure(text=f"Error: {error_msg}", text_color="#FF6B6B")
        self.weather_icon.configure(text="❌")
        self.city_label.configure(text="Error")
        self.temp_label.configure(text="--")
        self.weather_label.configure(text=error_msg)


if __name__ == "__main__":
    app = WeatherApp()
