from crop_oop import *
from weather_oop import *
import os
import time
from tqdm import tqdm


class Designs:
    def __init__(self):
        pass

    def display_ascii(self): # Clears the screen and displays the ASCII art logo

        self.clear_screen()
        print("""   
 █████╗  ██████╗ ██████╗ ██╗██╗      ██████╗  ██████╗ █████╗ ████████╗███████╗
██╔══██╗██╔════╝ ██╔══██╗██║██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝
███████║██║  ███╗██████╔╝██║██║     ██║   ██║██║     ███████║   ██║   █████╗  
██╔══██║██║   ██║██╔══██╗██║██║     ██║   ██║██║     ██╔══██║   ██║   ██╔══╝  
██║  ██║╚██████╔╝██║  ██║██║███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                                             """)
        for i in tqdm(range(100), desc="Loading", ascii=False, ncols=75):
            time.sleep(0.03)
        time.sleep(0.5)

    def clear_screen(self): # Clears the terminal screen
        os.system('cls')

    def main_menu_exit(self): # Prompts the user to go back to the main menu

        choice = input("\nEnter 'ok' to go back to main menu: ").lower()
        if choice == 'ok':
            for i in tqdm(range(100), desc="Loading", ascii=False, ncols=75):
                time.sleep(0.03)
            time.sleep(0.5)
            self.run()

class MenuOptions(Designs, WeatherData):
    def suggested_crop(self):
        """
        Displays the crop recommendation system.

        This method uses the WeatherData class to display the ranking of suggested crops based on weather and crop data.
        After displaying the results, it prompts the user to go back to the main menu.
        """
        self.clear_screen()
        print("Crop Recommendation System\n")

        crop_suggestion = WeatherData()
        suggestion = crop_suggestion.display_crop_ranking()

        self.main_menu_exit()


    def current_weather(self): # Displays the real-time weather update
        self.clear_screen()
        print("Real-time Weather Update\n")
        weather_bot = DisplayWeatherData()
        bot = weather_bot.display()

        self.main_menu_exit()

    def crop_price_calculator(self): # Calculates the estimated cost of agricultural land
        self.clear_screen()
        print("Agricultural Land Cost Estimator\n")
        area = int(input("Indicate Land Area in sqm: "))
        max_cost = 450
        min_cost = 100
        total_price = [min_cost*area, max_cost*area]
        print(f"An agricultural land in the Philippines costs {min_cost}-{max_cost} pesos")
        print(f"\nWith an area of {area}sqm, the estimated cost of land ranges from {total_price[0]} - {total_price[1]} pesos")

        self.main_menu_exit()

    def exit(self):
        self.clear_screen()
        self.display_ascii()
        print("\nThank you for using the program!\n")


    def about(self):
        self.clear_screen()
        print("About Page\n")
        print("Programmers:")
        print("Marc Linus D. Rosales")
        print("Gerard M. Malapote")
        print("Kristhian O. Pinili")
        print("Chester P. Lajara")

        self.main_menu_exit()


class MainMenu(MenuOptions, Designs):
    def __init__(self):
        MenuOptions.__init__(self)
        Designs.__init__(self)
        self.num_run = 0
        self.options = [
            ['A', "Crop Recommendation System"],
            ['B', 'Real-time Weather Update'],
            ['C', 'Agricultural Land Cost Estimator'],
            ['D', 'About'],
            ['E', 'Exit']
        ]


    def display_menu(self):
        self.clear_screen()
        print("Main Menu")
        print("Welcome to AgriLocate, Please select an option\n")
        for option in self.options:
            print(f"{option[0]} {option[1]}")
        

    def get_choice(self):
        self.display_menu()
        choice = input("\nEnter option: ").upper()
        selected_option = ""
        for option in self.options:
            if choice == option[0]:
                selected_option = choice
                break
                
        if selected_option == "":
            print("Invalid option. Please select a valid option.")
            time.sleep(1)
            self.clear_screen()
            self.get_choice()

        if selected_option == 'A':
            self.suggested_crop()
        elif selected_option == 'B':
            self.current_weather()
        elif selected_option == 'C':
            self.crop_price_calculator()
        elif selected_option == 'D':
            self.about()
        else:
            self.exit()

    def run(self): #this is the function that determines when the program would begin and stop
        self.state = True
        while self.state:
            if self.num_run == 0:
                self.num_run += 1
                self.display_ascii()
                self.get_choice()
            else:
                self.get_choice()
            
            self.state = False

menu = MainMenu()
menu.run()



