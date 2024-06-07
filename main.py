import requests
import tkinter as tk
from tkinter import ttk, messagebox

# API key 
api_key = 'dd7232eb58cc1d01901064ad96552b7d'

# Step 2: Weather Data Retrieval
def get_weather(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    current_data = response.json()

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    forecast_data = response.json()

    return current_data, forecast_data

# Step 3: User Interface
def show_weather():
    location = location_entry.get()
    try:
        current_data, forecast_data = get_weather(api_key, location)

        # Display current weather
        temperature = current_data['main']['temp']
        humidity = current_data['main']['humidity']
        wind_speed = current_data['wind']['speed']
        weather_description = current_data['weather'][0]['description']
        weather_icon = current_data['weather'][0]['icon']

        weather_info_label.config(text=f"Weather in {location}: {weather_description}\n"
                                        f"Temperature: {temperature}°C\n"
                                        f"Humidity: {humidity}%\n"
                                        f"Wind Speed: {wind_speed} m/s")

        icon_url = f"http://openweathermap.org/img/w/{weather_icon}.png"
        icon_response = requests.get(icon_url)
        icon_data = tk.PhotoImage(data=icon_response.content)
        weather_icon_label.config(image=icon_data)
        weather_icon_label.image = icon_data

        # Display forecast (next 5 days)
        forecast_info = "5-Day Forecast:\n"
        for forecast in forecast_data['list'][:5]:
            forecast_time = forecast['dt_txt']
            forecast_temperature = forecast['main']['temp']
            forecast_description = forecast['weather'][0]['description']
            forecast_info += f"{forecast_time}: {forecast_description}, {forecast_temperature}°C\n"

        forecast_label.config(text=forecast_info)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve weather data: {str(e)}")

root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

location_label = ttk.Label(root, text="Enter Location:")
location_label.pack(pady=10)

location_entry = ttk.Entry(root)
location_entry.pack(pady=5)

get_weather_button = ttk.Button(root, text="Get Weather", command=show_weather)
get_weather_button.pack(pady=5)

weather_info_label = ttk.Label(root, text="")
weather_info_label.pack(pady=10)

weather_icon_label = ttk.Label(root)
weather_icon_label.pack(pady=10)

forecast_label = ttk.Label(root, text="")
forecast_label.pack(pady=10)

root.mainloop()
