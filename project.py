"""
Welcome to Ruiz's final project submission for CS50P!
This program is a password creation and validation game.

Author: r._.uiz

Important Notes:
    This is my first Python program, so I apologize for any bad practices.
    Feel free to leave any feedback on how I can improve my code!
"""
import os  # Mainly for function clear_terminal()
import sys  # For exiting the program in all cases
import time  # For timing functions in rules and stats
import string  # For string-related functions in rules
import random  # For generating captcha and random Pokémon
import readline  # Mainly for easier input editing using arrow keys
import requests  # Mainly for PokeAPI calls
import pyperclip  # For copying to clipboard
from PIL import Image  # Mainly for displaying Pokémon sprite
from io import BytesIO  # For captcha file generation using captcha library
from pathlib import Path  # Mainly for accessing voice-related resources
from colorama import Fore, Style  # For colored terminal text styling
from captcha.audio import AudioCaptcha  # For audio captcha generation
from captcha.image import ImageCaptcha  # For image captcha generation
from datetime import datetime, timedelta  # For date/time-related functions/rules


class PywordGame:
    """
    This class implements the Py.word Game, a password creation and validation game.

    Rules:
    1. Password must be at least 5 characters long
    2. Password has a 50 character limit
    3. Password must include a number
    4. Password must contain a special character and no whitespace
    5. Password must contain an uppercase letter
    6. The digits in your password must add up to sum_digits variable
    7. Password must have the date today in `YYYY-MM-DD` format
    8. Password must include at least one of this Pokémon's type
    9. Password must include code in the `captcha.png`/`captcha.wav` in the same directory as this program
    10. Password must have the `flag emoji` of a country whose name/country code starts with the letter `P`
    11. Password must include the `month` we're currently in
    12. Password must have a `food emoji`
    13. Password must include the current time in `HH:MM` military time format

    If the password doesn't follow a rule, it will ask the user to try again
    until all requirements are met.
    """

    def __init__(self):
        """
        Initializes a new instance of the PywordGame class.

        Variables:
            captcha_options (str): A string containing lowercase letters and digits for captcha generation.
            captcha_range (int): The number of characters in the captcha.
            captcha (str): The generated captcha, pregenerated as the program initializes.
            voice_dir (Path): The directory for voice-related resources; captcha audio files.
            captcha_counter (int): The default-state counter for captcha attempts.
            captcha_attempt_limit (int): The limit for captcha attempts.
            poke_counter (int): The default-state counter for Pokémon-related attempts.
            poke_attempt_limit (int): The limit for Pokémon-related attempts.
            pokemon_types(List[str]): The default state for the Pokémon's type to avoid premature API calls.
            pokemon_name (str): The default state for the Pokémon's name to avoid premature API calls.
            min_length (int): The minimum length required for a valid password.
            max_length (int): The maximum character limit for a valid password.
            confirm_time_limit (int): The time limit in seconds for confirming the password.
            banner (str): A string containing an ASCII art banner for the game.

        Notes:
            The captcha is pregenerated as the program initializes.
            Variables with "# Difficulty" comments can be configured to change the difficulty of the game.
        """
        self.captcha_options = string.ascii_lowercase + string.digits
        self.captcha_range = 5  # Difficulty
        self.captcha = self.generate_captcha()
        self.voice_dir = Path.cwd() / "en"
        self.captcha_counter = 0  # Starting value
        self.captcha_attempt_limit = 5  # Difficulty
        self.poke_counter = 0  # Starting value
        self.poke_attempt_limit = 3  # Difficulty
        self.pokemon_types = None  # Don't change this
        self.pokemon_name = None  # Don't change this
        self.min_length = 5  # Difficulty
        self.max_length = 50  # Difficulty
        self.sum_digits = 69  # Difficulty
        self.confirm_time_limit = 30  # in seconds
        self.banner = """
        ┏┓┓┏ ┓ ┏┏┓┳┓┳┓  ┏┓┏┓┳┳┓┏┓
        ┃┃┗┫ ┃┃┃┃┃┣┫┃┃  ┃┓┣┫┃┃┃┣ 
        ┣┛┗┛•┗┻┛┗┛┛┗┻┛  ┗┛┛┗┛ ┗┗┛                                                                                                                                           
        """

    def main(self):
        """
        The entry point of the PywordGame class and the main looping process.

        Raises:
            KeyboardInterrupt: If the user presses Ctrl+C to quit the program.

        Variables:
            program_start_time (float): The start time of the program.
            attempt (str): The user's attempt at creating a password.
            program_elapsed_time (float): The elapsed time of the program.
            formatted_time (str): The formatted elapsed time of the program.

        Notes:
            Has ability to copy last attempt to clipboard.
            The program will automatically quit if the user successfully creates a password.
            Displays a success message with the elapsed time of the program.


        """
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
        """
        Clears the terminal screen, avoiding spamming the terminal with multiple lines of text
        """
        os.system("cls" if os.name == "nt" else "clear")

    def confirm(self, valid):
        """
        Prompt the user to reenter the valid password they created.

        Args:
            valid (str): The valid password created by the user.

        Returns:
            bool: True if the user enters the same password within the time limit, otherwise False.

        Variables:
            start_confirm_time (float): The start timer of the confirmation process.
            confirm_elapsed_time (float): The elapsed time of the confirmation process.
            confirm (str): The user's attempt at reentering the password.
        """
        confirm_start_time = time.time()
        pyperclip.copy("")
        print(
            f"{Fore.CYAN}ℹ You have {self.confirm_time_limit} seconds to manually reenter your password."
        )
        confirm = input(Fore.BLUE + "Reenter Password: " + Style.RESET_ALL)

        confirm_elapsed_time = time.time() - confirm_start_time

        if confirm == valid and confirm_elapsed_time <= self.confirm_time_limit:
            return True
        else:
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Password doesn't match or time limit exceeded. Please try again.{Style.RESET_ALL}."
            )
            return False

    def format_elapsed_time(self, elapsed_time):
        """
        Formats the elapsed time of the program into a human-readable format.
        """
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
        """
        Validates the password created by the user against the rules of the game.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password passes all the rules, otherwise False.

        Notes:
            If the password doesn't pass a rule, it will print the rule and return False.
        """
        return (
            self.min_length_reqs(s)
            and self.max_length_reqs(s)
            and self.has_number_reqs(s)
            and self.has_special_reqs(s)
            and self.has_upper_reqs(s)
            and self.sum_reqs(s)
            and self.date_today_reqs(s)
            and self.wild_pokemon_reqs(s)
            and self.captcha_reqs(s)
            and self.flag_reqs(s)
            and self.month_reqs(s)
            and self.food_reqs(s)
            and self.time_now_reqs(s)
        )

    def min_length_reqs(self, s):
        """
        The password must be at least 5 characters long.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password is at least 5 characters long, otherwise False.
        """
        if len(s) >= self.min_length:
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 1:{Style.RESET_ALL} Password must be at least {self.min_length} characters long"
            )
            return False

    def max_length_reqs(self, s):
        """
        The password has a 50 character limit.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password is at most 50 characters long, otherwise False.
        """
        if len(s) <= self.max_length:
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 2:{Style.RESET_ALL} Password has a {self.max_length} character limit"
            )
            return False

    def has_number_reqs(self, s):
        """
        The password must include a number.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password includes a number, otherwise False.
        """
        if any(char.isdigit() for char in s):
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 3:{Style.RESET_ALL} Password must include a number."
            )
            return False

    def has_special_reqs(self, s):
        """
        The password must contain a special character and no whitespace.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password contains a special character and no whitespace, otherwise False.
        """
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
        """
        The password must contain an uppercase letter.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password contains an uppercase letter, otherwise False.
        """
        if any(char.isupper() for char in s):
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 5:{Style.RESET_ALL} Password must contain an uppercase letter."
            )
            return False

    def sum_reqs(self, s):
        """
        The digits in your password must add up to the sum_digits variable whose default is 69.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the digits in the password add up to the sum_digits variable, otherwise False.

        Variables:
            digit_sum (int): The sum of the digits in the password.
        """
        digit_sum = sum(int(char) for char in s if char.isdigit())
        if digit_sum == self.sum_digits:
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 6:{Style.RESET_ALL} The digits in your password must add up to `{self.sum_digits}`."
                # f"\n{Style.DIM} (Current sum: {digit_sum}){Style.RESET_ALL}" # Will this be too easy?
            )
            return False

    def date_today_reqs(self, s):
        """
        The password must have the date today in `YYYY-MM-DD` format.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password has the date today in `YYYY-MM-DD` format, otherwise False.

        Variables:
            str_today (str): The date today in `YYYY-MM-DD` format.
        """
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
        """
        Fetches a random Pokémon from the PokeAPI.

        Returns:
            tuple: A tuple containing the Pokémon's types and name.

        Variables:
            poke_index (int): A random integer between 1 and 1021, as there are 1021 Pokémon in the PokeAPI.
            response (Response): The response from the PokeAPI.
            pokemon_data (dict): The JSON response from the PokeAPI.
            pokemon_name (str): The name of the Pokémon chosen randomly.
            pokemon_types (List[str]): The type/s of the Pokémon.
            pokemon_sprite_url (str): The URL of the Pokémon's sprite.
            img (Image): The sprite of the Pokémon.

        Notes:
            If the PokeAPI call fails, it will default to Bulbasaur's type/s.
            This shows the user the Pokémon's sprite {img} through PIL.
        """
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
        """
        Resets the Pokémon to a new random Pokémon and resets the poke_counter.

        Variables:
            poke_counter (int): The counter for Pokémon-related attempts. This is reset to 0.
            pokemon_types (List[str]): The type/s of the Pokémon generated randomly.
            pokemon_name (str): The name of the Pokémon generated randomly.
            fetch_random_pokemon (tuple): A tuple containing the generated Pokémon's type/s and name.

        Notes:
            Only called when the poke_counter reaches the poke_attempt_limit.
        """
        self.poke_counter = 0
        self.pokemon_types, self.pokemon_name = self.fetch_random_pokemon()

    def wild_pokemon_reqs(self, s):
        """
        Password must include at least one of the Pokémon's type.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password includes at least one of the Pokémon's type, otherwise False.

        Variables:
            type (str): The Pokémon's type checked against the password.
            pokemon_types (List[str]): The type/s of the Pokémon generated randomly.
            pokemon_name (str): The name of the Pokémon generated randomly.
            poke_counter (int): The counter for Pokémon-related attempts.
            poke_countdown (int): The number of attempts left before the Pokémon is reset.
            poke_attempt_limit (int): The limit for Pokémon-related attempts.
        Notes:
            If the Pokémon's type is None (which, for the first iteration over the function, it will be), it will generate a random Pokémon.
            Once the Pokémon's type is generated, it will check if the Pokémon's type is in the password.
            If the Pokémon's type is not in the password, it will increment the poke_counter.
            If the poke_counter reaches the poke_attempt_limit, it will reset the Pokémon through reset_pokemon().
            Casefold is used to ignore case sensitivity.
        """
        if self.pokemon_types is None:
            self.fetch_random_pokemon()
            return False
        for type in self.pokemon_types:
            if type.casefold() not in s.casefold():
                self.poke_counter += 1
                poke_countdown = self.poke_attempt_limit - self.poke_counter
                self.clear_terminal()
                print(
                    f"{Fore.RED}{Style.BRIGHT}❗ Rule 8:{Style.RESET_ALL} A wild {Style.BRIGHT}{self.pokemon_name}{Style.RESET_ALL} appeared!\n"
                    f"Your password must include at least one of this Pokémon's type.\n"
                    f"{Style.DIM}(Regenerates in {poke_countdown} wrong type attempts){Style.RESET_ALL}"
                )
                if self.poke_counter == self.poke_attempt_limit:
                    self.reset_pokemon()
                    print("New Pokémon!")
                return False
            return True

    def generate_captcha(self):
        """
        Generates a captcha using the captcha_options and captcha_range variables.

        Returns:
            str: The generated captcha.

        Variables:
            captcha_options (str): A string containing lowercase letters and digits for captcha generation.
            captcha_range (int): The number of characters in the captcha.
        """
        return "".join(
            random.choice(self.captcha_options) for _ in range(self.captcha_range)
        )

    def generate_audio_captcha(self):
        """
        Generates an audio captcha.

        Variables:
            voice_dir (Path): The directory for voice-related resources; captcha audio files.
            audio (AudioCaptcha): The audio captcha generator.
            data (BytesIO): The audio captcha data.
            captcha (str): The generated captcha from generate_captcha().
        Notes:
            Utilizes the captcha library.
            The audio captcha is generated as `captcha.wav` in the same directory as this program.
        """
        audio = AudioCaptcha(str(self.voice_dir))
        data = audio.generate(self.captcha)
        audio.write(self.captcha, "captcha.wav")

    def generate_image_captcha(self):
        """
        Generates an image captcha.

        Variables:
            image (ImageCaptcha): The image captcha generator.
            data (BytesIO): The image captcha data.
            captcha (str): The generated captcha from generate_captcha().

        Notes:
            Utilizes the captcha library.
            The image captcha is generated as `captcha.png` in the same directory as this program.
        """
        image = ImageCaptcha()
        data = image.generate(self.captcha)
        image.write(self.captcha, "captcha.png")

    def reset_captcha(self):
        """
        Resets the captcha.

        Variables:
            captcha_counter (int): The default-state counter for captcha attempts. This is reset to 0.
            captcha (str): The generated captcha from generate_captcha().

        Notes:
            Only called when the captcha_counter reaches the captcha_attempt_limit.
            The captcha is regenerated.
            The audio captcha is regenerated.
            The image captcha is regenerated.
        """
        self.captcha_counter = 0
        self.captcha = self.generate_captcha()
        self.generate_audio_captcha()
        self.generate_image_captcha()

    def captcha_reqs(self, s):
        """
        The password must include code in the `captcha.png`/`captcha.wav` in the same directory as this program.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password includes the captcha, otherwise False.

        Variables:
            captcha (str): The generated captcha from generate_captcha().
            captcha_counter (int): The counter for captcha attempts.
            captcha_attempt_limit (int): The limit for captcha attempts.
            captcha_countdown (int): The number of attempts left before the captcha is reset.

        Notes:
            If the captcha is not in the password, it will increment the captcha_counter.
            If the captcha_counter reaches the captcha_attempt_limit, it will reset the captcha through reset_captcha().
        """
        if self.captcha not in s:
            self.captcha_counter += 1
            captcha_countdown = self.captcha_attempt_limit - self.captcha_counter
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 9:{Style.RESET_ALL} Password must include code in the {Fore.RED}`captcha.png`/`captcha.wav`{Style.RESET_ALL} in the same directory as this program.\n"
                f"{Style.DIM}Regenerates in {captcha_countdown} wrong captcha attempts.{Style.RESET_ALL}"
            )
            if self.captcha_counter == self.captcha_attempt_limit:
                print("Captcha reset!")
                self.reset_captcha()
            return False
        return True

    def flag_reqs(self, s):
        """
        Password must have the `flag emoji` of a country whose name/country code starts with the letter `P`.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password includes a flag emoji of a country whose name/country code starts with the letter `P`, otherwise False.

        Variables:
            list_valid_flag (List[str]): A list of valid flag emojis of countries whose name/country code starts with the letter `P`.

        Notes:
            The list of valid flag emojis is stored in `validFlag.txt`.
        """
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
        """
        Password must include the `month` we're currently in.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password includes the `month` we're currently in, otherwise False.

        Variables:
            str_month (str): The month we're currently in.

        Notes:
            The current month is fetched using datetime.now().
            Casefold is used to ignore case sensitivity.
        """
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
        """
        The password must have a `food emoji`.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password has a `food emoji`, otherwise False.

        Variables:
            list_valid_food (List[str]): A list of valid food emojis.

        Notes:
            The list of valid food emojis is stored in `validFood.txt`.
        """
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
        """
        The password must include the current time in `HH:MM` military time format.

        Args:
            s (str): The password created by the user.

        Returns:
            bool: True if the password includes the current time in `HH:MM` military time format, otherwise False.

        Variables:
            str_time (str): The current time in `HH:MM` military time format.

        Notes:
            The current time is fetched using datetime.now().
            Casefold is used to ignore case sensitivity.
        """
        str_time = datetime.now().strftime("%H:%M")
        if str_time.casefold() in s.casefold():
            return True
        else:
            self.clear_terminal()
            print(
                f"{Fore.RED}{Style.BRIGHT}✘ Rule 13:{Style.RESET_ALL} Password must include the current time in `HH:MM` military time format."
            )
            return False


if __name__ == "__main__":
    """
    Generates the audio captcha and image captcha before running the main program.
    """
    game = PywordGame()
    game.generate_audio_captcha()
    game.generate_image_captcha()
    game.main()
