from crop_oop import *
import os
class DisplayWeatherData(WeatherData):
    def __init__(self):
        WeatherData.__init__(self)

    def display(self):
        """
        DisplayWeatherData class is used to display weather data based on user input.

        This class extends the WeatherData class and inherits its functionality.
        """

        self.get_current_weather() # Get current weather data
        print(f"\nWeather Update in {self.user_input}\n")

        self.apparent_temperature = self.response.json()['hourly']['apparent_temperature'][0] # Get apparent temperature
        self.rain_probability = self.response.json()['hourly']['precipitation_probability'][0] # Get precipitation probability
        if self.user_input != None:
            print(f"Temperature: {self.current_temperature}C")
            print(f"Apparent Temperature: {self.apparent_temperature}C")
            print(f"precipitation: {self.current_rainfall}mm")
            print(f"Precipitation Probability: {self.rain_probability}%")
            print(f"Humidity: {self.current_humidity}")
            
        else:
            print("Can't display weather data without your city input")