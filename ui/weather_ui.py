# To create graphical user interface used Tkinter
import sys
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

# Ensure the project root is on sys.path so sibling packages are importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.weather_service import fetch_weather


root = tk.Tk()
root.title("Weather App")
root.geometry("500x420")
root.resizable(False, False)

heading_font = tkfont.Font(family="Arial", size=20, weight="bold")
label_font = tkfont.Font(family="Arial", size=12)

title_label = tk.Label(root, text="Weather App", font=heading_font)
title_label.pack(pady=12)

input_frame = tk.Frame(root)
input_frame.pack(pady=8)

city_entry = tk.Entry(input_frame, width=30, font=label_font)
city_entry.insert(0, "Colombo")
city_entry.grid(row=0, column=0, padx=(0, 8))

def on_search(event=None):
    city = city_entry.get().strip()
    if not city:
        messagebox.showinfo("Input required", "Please enter a city name.")
        return

    search_button.config(state="disabled")
    root.update_idletasks()

    data = fetch_weather(city)

    search_button.config(state="normal")

    if "error" in data:
        messagebox.showerror("Error", data.get("details") or data.get("error"))
        clear_results()
        return

    show_results(data)


search_button = tk.Button(input_frame, text="Get Weather", command=on_search, width=12)
search_button.grid(row=0, column=1)

city_entry.bind("<Return>", on_search)

result_frame = tk.Frame(root, padx=20, pady=12)
result_frame.pack(fill="x")

city_label = tk.Label(result_frame, text="", font=("Arial", 14, "bold"))
city_label.pack(anchor="w")

temp_label = tk.Label(result_frame, text="", font=label_font)
temp_label.pack(anchor="w", pady=(6, 0))

humidity_label = tk.Label(result_frame, text="", font=label_font)
humidity_label.pack(anchor="w")

weather_label = tk.Label(result_frame, text="", font=label_font)
weather_label.pack(anchor="w")

wind_label = tk.Label(result_frame, text="", font=label_font)
wind_label.pack(anchor="w")


def clear_results():
    city_label.config(text="")
    temp_label.config(text="")
    humidity_label.config(text="")
    weather_label.config(text="")
    wind_label.config(text="")


def show_results(data: dict):
    city_name = data.get("name", "-")
    temperature = data.get("main", {}).get("temp", "-")
    humidity = data.get("main", {}).get("humidity", "-")
    weather = data.get("weather", [{}])[0].get("main", "-")
    wind_speed = data.get("wind", {}).get("speed", "-")

    city_label.config(text=f"City: {city_name}")
    temp_label.config(text=f"Temperature: {temperature}°C")
    humidity_label.config(text=f"Humidity: {humidity}%")
    weather_label.config(text=f"Weather: {weather}")
    wind_label.config(text=f"Wind Speed: {wind_speed} m/s")


if __name__ == "__main__":
    # Optionally pre-fill and show initial data
    try:
        show_results(fetch_weather(city_entry.get()))
    except Exception:
        clear_results()

    root.mainloop()