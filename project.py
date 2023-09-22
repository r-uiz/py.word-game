import sys
import string
import random
import readline
import requests
import pyperclip
from io import BytesIO
from pathlib import Path
from datetime import datetime
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from PIL import Image


def main():
    # explanation
    print("Welcome to Py.word Game! Choose a password.")
    print("Ctrl+C to quit the program")
    # ask for attempt
    try:
        while True:
            attempt = input("Password: ").strip()
            pyperclip.copy(attempt)
            if validate(attempt):
                sys.exit(
                    f'Congrats! Password "{attempt}" is valid. Wait... did we say that out loud?'
                )
            else:
                print(
                    "Last attempt copied to clipboard. Attempt again or Ctrl+C to quit."
                )
    except KeyboardInterrupt:
        print("\nProgram quit. Try to create a password again later!")


def validate(s):
    return (
        min_length_reqs(s)
        and max_length_reqs(s)
        and has_number_reqs(s)
        and has_special_reqs(s)
        and has_upper_reqs(s)
        and six_nine_reqs(s)
        and date_today_reqs(s)
        and wild_pokemon_reqs(s)
        and captcha_reqs(s)
        and flag_reqs(s)
        and month_reqs(s)
        and food_reqs(s)
        and time_now_reqs(s)
    )


def min_length_reqs(s):
    # min 5
    if len(s) >= 5:
        return True
    else:
        print("Rule 1: Password must be at least 5 characters long")
        return False


def max_length_reqs(s):
    # max 50
    if len(s) <= 50:
        return True
    else:
        print("Rule 2: Password has a 50 character limit")
        return False


def has_number_reqs(s):
    # include a number
    if any(char.isdigit() for char in s):
        return True
    else:
        print("Rule 3: Password must include a number.")
        return False


def has_special_reqs(s):
    special_characters = set(string.punctuation)
    if any(char in special_characters for char in s) and not any(
        char.isspace() for char in s
    ):
        return True
    else:
        print("Rule 4: Password must contain a special character and no whitespace.")
        return False


def has_upper_reqs(s):
    # has an uppercase letter
    if any(char.isupper() for char in s):
        return True
    else:
        print("Rule 5: Password must contain an uppercase letter.")
        return False


def six_nine_reqs(s):
    digit_sum = sum(int(char) for char in s if char.isdigit())
    if digit_sum == 69:
        return True
    else:
        print("Rule 6: The digits in your password must add up to `69`.")
        return False


def date_today_reqs(s):
    str_today = datetime.now().strftime("%Y-%m-%d")
    if str_today in s:
        return True
    else:
        print("Rule 7: Password must have the date today in `YYYY-MM-DD` format.")
        return False


def fetch_random_pokemon():
    global pokemon_types, pokemon_name
    poke_index = random.randrange(1, 1021)
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_index}")

    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_name = pokemon_data["name"].title()
        pokemon_types = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
        pokemon_sprite_url = pokemon_data["sprites"]["other"]["official-artwork"][
            "front_default"
        ]

        img = Image.open(requests.get(pokemon_sprite_url, stream=True).raw)
        img.show(title=pokemon_name)
        print(
            f"Rule 8: A wild {pokemon_name} appeared! Your password must include at least one of this Pokémon's type."
        )
        return pokemon_types

    else:
        print(
            f"\nError: PokeAPI call failed. Error Code {response.status_code}. By default, get the type/s of Bulbasaur instead."
        )
        return ["grass", "poison"]


def reset_pokemon():
    global poke_counter, pokemon_types, pokemon_name
    poke_counter = 0
    pokemon_types = fetch_random_pokemon()
    pokemon_name = pokemon_types[0]


def wild_pokemon_reqs(s):
    global poke_counter, pokemon_types, pokemon_name
    if pokemon_types is None:
        fetch_random_pokemon()
        return False
    for type in pokemon_types:
        if type not in s:
            poke_counter += 1
            poke_countdown = 3 - poke_counter
            print(
                f"Rule 8: A wild {pokemon_name} appeared! Your password must include at least one of this Pokémon's type.(Regenerates in {poke_countdown} wrong type attempts)"
            )
            if poke_counter == 3:
                reset_pokemon()
                print("New Pokémon!")
            return False
        return True


def generate_audio_captcha():
    audio = AudioCaptcha(str(voice_dir))
    data = audio.generate(captcha)
    audio.write(captcha, "captcha.wav")


def generate_image_captcha():
    image = ImageCaptcha()
    data = image.generate(captcha)
    image.write(captcha, "captcha.png")


def reset_captcha():
    global captcha, captcha_counter
    captcha_counter = 0
    captcha = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
    generate_audio_captcha()
    generate_image_captcha()


def captcha_reqs(s):
    global captcha, captcha_counter
    if captcha not in s:
        captcha_counter += 1
        captcha_countdown = 5 - captcha_counter
        print(
            f"Rule 9: Password must include the captcha in the `captcha.png`/`captcha.wav` in the same directory as this program. Regenerates in {captcha_countdown} wrong captcha attempts."
        )
        if captcha_counter == 5:
            print("Captcha reset!")
            reset_captcha()
        return False
    return True


def flag_reqs(s):
    with open("validFlag.txt") as file:
        list_valid_flag = file.read().splitlines()

    # if s contains valid flag
    if any(char in s for char in list_valid_flag):
        return True
    else:
        print(
            "Rule 10: Password must have the `flag emoji` of a country whose name/country code starts with the letter `P`."
        )
        return False


def month_reqs(s):
    str_month = datetime.now().strftime("%B")
    if str_month.casefold() in s.casefold():
        return True
    else:
        print("Rule 11: Password must include the `month` we're currently in.")
        return False


def food_reqs(s):
    # food item emoji list
    with open("validFood.txt") as file:
        list_valid_food = file.read().splitlines()

    if any(char in s for char in list_valid_food):
        return True
    else:
        print(
            "Rule 12: We've been here for so long… I'm hungry! Password must have a `food emoji`."
        )
        return False


def time_now_reqs(s):
    str_time = datetime.now().strftime("%H:%M")
    if str_time.casefold() in s.casefold():
        return True
    else:
        print(
            "Rule 13: Your password must include the current time in `HH:MM` military time format."
        )
        return False


if __name__ == "__main__":
    captcha_counter = 0
    voice_dir = Path.cwd() / "en"
    captcha = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
    poke_counter = 0
    pokemon_types = None
    pokemon_name = None
    generate_audio_captcha()
    generate_image_captcha()
    main()
