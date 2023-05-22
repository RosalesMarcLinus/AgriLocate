import pandas as pd
import requests


class ReadCityCSV:
    def __init__(self):
        """
        ReadCityCSV class reads city data from a CSV file and provides methods to retrieve city coordinates.
        """
         
        self.df = pd.read_csv("worldcities.csv")
        self.selected_df = self.df[['city', 'country', 'lat', 'lng']]
        self.selected_dict = self.selected_df.to_dict() # Convert selected data to a dictionary

    def retrieve_coordinates(self):
        self.user_input = input("Enter city name (Enter 'None' if coordinates): ").title()
        country_idx = 0

        for idx, val in self.selected_dict['city'].items():
            if self.user_input == None:
                break
            elif self.user_input == val:
                country_idx = idx

        if country_idx != 0:
            self.latitude = self.selected_dict['lat'][country_idx]
            self.longitude = self.selected_dict['lng'][country_idx]
        elif country_idx == 0:
            self.latitude_input = input("\nLocation Latitude: ")
            self.longitude_input = input("Location Longitude: ")
            self.latitude = self.latitude_input
            self.longitude = self.longitude_input
            self.user_input = f"Latitude: {self.latitude_input}, Longitude: {self.longitude_input}"


class ReadCropCSV:
    def __init__(self):
        """
        ReadCropCSV class reads crop data from a CSV file and provides methods to retrieve crop data.
        """    
        self.crop_df = pd.read_csv("Crop_recommendation.csv")

    def get_crop_data(self):
        self.crop_group = self.crop_df.groupby('label') # Group data by crop label
        self.temp_df = self.crop_group.describe()['temperature'] # Calculate statistics for temperature
        self.humidity_df = self.crop_group.describe()['humidity'] # Calculate statistics for humidity
        self.rainfall_df = self.crop_group.describe()['rainfall'] # Calculate statistics for rainfall

    def crop_data_todict(self):
        self.get_crop_data()
        self.temp_dict = self.temp_df.to_dict() # Convert temperature data to a dictionary
        self.humidity_dict = self.humidity_df.to_dict() # Convert humidity data to a dictionary
        self.rainfall_dict = self.rainfall_df.to_dict() # Convert rainfall data to a dictionary
        self.unique_crop_labels = sorted(self.crop_df['label'].unique()) # Get unique crop labels


class WeatherData(ReadCityCSV, ReadCropCSV):
    def __init__(self):
        """
        WeatherData class retrieves and processes weather and crop data based on user input.
        """
        ReadCityCSV.__init__(self) # Call ReadCityCSV's __init__ method explicitly
        ReadCropCSV.__init__(self) # Call ReadCropCSV's __init__ method explicitly

        self.api = "https://api.open-meteo.com/v1/forecast" # Weather data API URL

    def set_city_coords(self):
        self.retrieve_coordinates() # Retrieve city coordinates from user input
        self.parameter = {
            "latitude": self.latitude, "longitude": self.longitude,
            "hourly": ["temperature_2m", "relativehumidity_2m", "apparent_temperature",
                       "precipitation", "precipitation_probability", "soil_temperature_0cm"]}
        self.response = requests.get(url=self.api, params=self.parameter)
        self.hourly_weather_data = self.response.json()['hourly']

    def get_current_weather(self):
        self.set_city_coords()
        self.current_temperature = self.hourly_weather_data['temperature_2m'][0]
        self.current_humidity = self.hourly_weather_data['relativehumidity_2m'][0]
        self.current_rainfall = self.hourly_weather_data['precipitation'][0]
        self.crop_data_todict()

    def crop_score_computation(self):
        self.get_current_weather()

        crop_score_results = {}
        crop_score_results_wvar = {}

        import numpy as np

        # zscore normalization
        # Compute mean and standard deviation
        temp_mean = np.mean(list(self.temp_dict['mean'].values()))
        temp_std = np.std(list(self.temp_dict['mean'].values()))

        hum_mean = np.mean(list(self.humidity_dict['mean'].values()))
        hum_std = np.std(list(self.humidity_dict['mean'].values()))

        rain_mean = np.mean(list(self.rainfall_dict['mean'].values()))
        rain_std = np.std(list(self.rainfall_dict['mean'].values()))

        for idx, val in enumerate(self.unique_crop_labels):
            temp_computation = abs((int(self.temp_dict['mean'][val]) - int(self.current_temperature)) / temp_std)
            hum_computation = abs((int(self.humidity_dict['mean'][val]) - int(self.current_humidity)) / hum_std)
            rain_computation = abs((int(self.rainfall_dict['mean'][val]) - int(self.current_rainfall)) / rain_std)
            crop_score_results[val] = {'temp_mean': temp_computation, 'rain_mean': rain_computation, 'hum_mean': hum_computation}
            crop_score_results_wvar[val] = [val, temp_computation, hum_computation, rain_computation]

        self.crop_ranking_list = []

        for idx, val in enumerate(self.unique_crop_labels):
            self.crop_ranking_list.append(crop_score_results_wvar[val]) # Create a list of crops with scores

        self.crop_ranking_list = sorted(self.crop_ranking_list, key=lambda x: (x[1], x[3], x[2]), reverse=False) # Sort crop ranking list
    
    def display_crop_ranking(self):
        self.crop_score_computation() # Compute crop scores
        print(f"Latitude: {self.latitude}, Longitude: {self.longitude}")
        print(f"\nRanking of the Best Suitable Crop in {self.user_input}\n")
        if self.crop_ranking_list:
            for idx, val in enumerate(self.crop_ranking_list):
                if idx < 5:
                    print(f"Top {idx+1}: {val[0]}") # Display top crops based on ranking

