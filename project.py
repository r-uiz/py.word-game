import os
import sys
import time
import string
import random
import readline
import requests
import pyperclip
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from colorama import Fore, Style
from PIL import Image


class PasswordGame:
    def __init__(self) -> None:
        self.captcha_options = string.ascii_lowercase + string.digits
        self.captcha_range = 5
        self.captcha = self.generate_captcha()
        self.voice_dir = Path.cwd() / "en"
        self.captcha_counter = 0
        self.poke_counter = 0
        self.pokemon_types = None
        self.pokemon_name = None
        self.min_length = 5
        self.max_length = 50
        self.confirm_time_limit = 30  # in seconds
        self.banner = """
        ┏┓┓┏ ┓ ┏┏┓┳┓┳┓  ┏┓┏┓┳┳┓┏┓
        ┃┃┗┫ ┃┃┃┃┃┣┫┃┃  ┃┓┣┫┃┃┃┣ 
        ┣┛┗┛•┗┻┛┗┛┛┗┻┛  ┗┛┛┗┛ ┗┗┛                                                                                                                                           
        """

    def main(self):
        print(Fore.GREEN + self.banner + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + "Welcome to Py.word Game! Choose a password."
            + Style.RESET_ALL
        )
        program_start_time = time.time()
        try:
            while True:
                attempt = input(Fore.BLUE + "Password: " + Style.RESET_ALL).strip()
                if self.validate(attempt):
                    if self.confirm(attempt):
                        break
                else:
                    pyperclip.copy(attempt)
                    print(
                        Style.DIM
                        + "Last attempt copied to clipboard. Attempt again or Ctrl+C to quit."
                        + Style.RESET_ALL
                    )
        except KeyboardInterrupt:
            self.clear_terminal()
            print(
                Style.BRIGHT
                + "Program quit. Try to create a password again later!"
                + Style.RESET_ALL
            )
            sys.exit()
        program_elapsed_time = time.time() - program_start_time
        formatted_time = self.format_elapsed_time(program_elapsed_time)
        self.clear_terminal()
        print(Fore.GREEN + self.banner + Style.RESET_ALL)
        sys.exit(
            f"{Fore.GREEN}{Style.BRIGHT}✔ Congrats!{Style.NORMAL} Successfully created a password in {formatted_time}!\n"
            f'Password {Style.BRIGHT}"{attempt}"{Style.NORMAL} is valid.\n'
            f"{Style.DIM}Wait... did we say that out loud?{Style.RESET_ALL}"
        )

    def clear_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")

    def confirm(self, valid):
        start_confirm_time = time.time()
        pyperclip.copy("")
        print(
            f"{Fore.CYAN}ℹ You have {self.confirm_time_limit} seconds to manually reenter your password."
        )
        confirm = input(Fore.BLUE + "Reenter Password: " + Style.RESET_ALL)

        confirm_elapsed_time = time.time() - start_confirm_time

        if confirm == valid and confirm_elapsed_time <= self.confirm_time_limit:
            return True
        else:
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Password doesn't match or time limit exceeded. Please try again.{Style.RESET_ALL}."
            )
            return False

    def format_elapsed_time(self, elapsed_time):
        elapsed_time = int(elapsed_time)
        td = timedelta(seconds=elapsed_time)
        days, seconds = td.days, td.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        formatted_time = ""

        if days:
            formatted_time += f"{days} days, "
        if hours:
            formatted_time += f"{hours} hours, "
        if minutes:
            formatted_time += f"{minutes} minutes, "
        formatted_time += f"{seconds} seconds"

        return formatted_time

    def validate(self, s):
        return (
            self.min_length_reqs(s)
            and self.max_length_reqs(s)
            and self.has_number_reqs(s)
            and self.has_special_reqs(s)
            and self.has_upper_reqs(s)
            and self.six_nine_reqs(s)
            and self.date_today_reqs(s)
            and self.wild_pokemon_reqs(s)
            and self.captcha_reqs(s)
            and self.flag_reqs(s)
            and self.month_reqs(s)
            and self.food_reqs(s)
            and self.time_now_reqs(s)
        )

    def min_length_reqs(self, s):
        if len(s) >= self.min_length:
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 1:{Style.RESET_ALL} Password must be at least {self.min_length} characters long"
            )
            return False

    def max_length_reqs(self, s):
        if len(s) <= self.max_length:
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 2:{Style.RESET_ALL} Password has a {self.max_length} character limit"
            )
            return False

    def has_number_reqs(self, s):
        # include a number
        if any(char.isdigit() for char in s):
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 3:{Style.RESET_ALL} Password must include a number."
            )
            return False

    def has_special_reqs(self, s):
        special_characters = set(string.punctuation)
        if any(char in special_characters for char in s) and not any(
            char.isspace() for char in s
        ):
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 4:{Style.RESET_ALL} Password must contain a special character and no whitespace."
            )
            return False

    def has_upper_reqs(self, s):
        # has an uppercase letter
        if any(char.isupper() for char in s):
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 5:{Style.RESET_ALL} Password must contain an uppercase letter."
            )
            return False

    def six_nine_reqs(self, s):
        digit_sum = sum(int(char) for char in s if char.isdigit())
        if digit_sum == 69:
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 6:{Style.RESET_ALL} The digits in your password must add up to `69`."
            )
            return False

    def date_today_reqs(self, s):
        str_today = datetime.now().strftime("%Y-%m-%d")
        if str_today in s:
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 7:{Style.RESET_ALL} Password must have the date today in `YYYY-MM-DD` format."
            )
            return False

    def fetch_random_pokemon(self):
        poke_index = random.randrange(1, 1021)
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_index}")

        if response.status_code == 200:
            pokemon_data = response.json()
            self.pokemon_name = pokemon_data["name"].title()
            self.pokemon_types = [
                type_data["type"]["name"] for type_data in pokemon_data["types"]
            ]
            pokemon_sprite_url = pokemon_data["sprites"]["other"]["official-artwork"][
                "front_default"
            ]

            img = Image.open(requests.get(pokemon_sprite_url, stream=True).raw)
            img.show(title=self.pokemon_name)
            self.clear_terminal()
            print(
                f"{Fore.CYAN}{Style.BRIGHT}❗ Rule 8:{Style.RESET_ALL} A wild {Style.BRIGHT}{self.pokemon_name}{Style.RESET_ALL} appeared!\n"
                f"Your password must include at least one of this Pokémon's type."
            )
            return self.pokemon_types, self.pokemon_name

        else:
            self.clear_terminal()
            print(
                f"\nError: PokeAPI call failed. Error Code {response.status_code}. By default, include the type/s of Bulbasaur instead."
            )
            return ["grass", "poison"]

    def reset_pokemon(self):
        self.poke_counter = 0
        self.pokemon_types, self.pokemon_name = self.fetch_random_pokemon()

    def wild_pokemon_reqs(self, s):
        if self.pokemon_types is None:
            self.fetch_random_pokemon()
            return False
        for type in self.pokemon_types:
            if type not in s:
                self.poke_counter += 1
                poke_countdown = 3 - self.poke_counter
                self.clear_terminal()
                print(
                    f"{Fore.RED}{Style.BRIGHT}❗ Rule 8:{Style.RESET_ALL} A wild {Style.BRIGHT}{self.pokemon_name}{Style.RESET_ALL} appeared!\n"
                    f"Your password must include at least one of this Pokémon's type.\n"
                    f"{Style.DIM}(Regenerates in {poke_countdown} wrong type attempts){Style.RESET_ALL}"
                )
                if self.poke_counter == 3:
                    self.reset_pokemon()
                    print("New Pokémon!")
                return False
            return True

    def generate_captcha(self):
        return "".join(
            random.choice(self.captcha_options) for _ in range(self.captcha_range)
        )

    def generate_audio_captcha(self):
        audio = AudioCaptcha(str(self.voice_dir))
        data = audio.generate(self.captcha)
        audio.write(self.captcha, "captcha.wav")

    def generate_image_captcha(self):
        image = ImageCaptcha()
        data = image.generate(self.captcha)
        image.write(self.captcha, "captcha.png")

    def reset_captcha(self):
        self.captcha_counter = 0
        self.captcha = self.generate_captcha()
        self.generate_audio_captcha()
        self.generate_image_captcha()

    def captcha_reqs(self, s):
        if self.captcha not in s:
            self.captcha_counter += 1
            captcha_countdown = 5 - self.captcha_counter
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 9:{Style.RESET_ALL} Password must include code in the {Fore.RED}`captcha.png`/`captcha.wav`{Style.RESET_ALL} in the same directory as this program.\n"
                f"{Style.DIM}Regenerates in {captcha_countdown} wrong captcha attempts.{Style.RESET_ALL}"
            )
            if self.captcha_counter == 5:
                print("Captcha reset!")
                self.reset_captcha()
            return False
        return True

    def flag_reqs(self, s):
        with open("validFlag.txt") as file:
            list_valid_flag = file.read().splitlines()

        # if s contains valid flag
        if any(char in s for char in list_valid_flag):
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 10:{Style.RESET_ALL} Password must have the `flag emoji` of a country whose name/country code starts with the letter `P`."
            )
            return False

    def month_reqs(self, s):
        str_month = datetime.now().strftime("%B")
        if str_month.casefold() in s.casefold():
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 11:{Style.RESET_ALL} Password must include the `month` we're currently in."
            )
            return False

    def food_reqs(self, s):
        # food item emoji list
        with open("validFood.txt") as file:
            list_valid_food = file.read().splitlines()

        if any(char in s for char in list_valid_food):
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 12:{Style.RESET_ALL} We've been here for so long… I'm hungry! Password must have a `food emoji`."
            )
            return False

    def time_now_reqs(self, s):
        str_time = datetime.now().strftime("%H:%M")
        if str_time.casefold() in s.casefold():
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 13:{Style.RESET_ALL} Your password must include the current time in `HH:MM` military time format."
            )
            return False


if __name__ == "__main__":
    game = PasswordGame()
    game.generate_audio_captcha()
    game.generate_image_captcha()
    game.main()
