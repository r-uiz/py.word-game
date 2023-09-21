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
        minLength_reqs(s)
        and maxLength_reqs(s)
        and hasNumber_reqs(s)
        and hasSpecial_reqs(s)
        and hasUpper_reqs(s)
        and sixNine_reqs(s)
        and dateToday_reqs(s)
        and wildPokemon_reqs(s)
        and captcha_reqs(s)
        and flag_reqs(s)
        and month_reqs(s)
        and food_reqs(s)
        and timeNow_reqs(s)
    )


def minLength_reqs(s):
    # min 5
    if len(s) >= 5:
        return True
    else:
        print("Rule 1: Password must be at least 5 characters long")
        return False


def maxLength_reqs(s):
    # max 50
    if len(s) <= 50:
        return True
    else:
        print("Rule 2: Password has a 50 character limit")
        return False


def hasNumber_reqs(s):
    # include a number
    if any(char.isdigit() for char in s):
        return True
    else:
        print("Rule 3: Password must include a number.")
        return False


def hasSpecial_reqs(s):
    specialCharacters = set(string.punctuation)
    if any(char in specialCharacters for char in s) and not any(
        char.isspace() for char in s
    ):
        return True
    else:
        print("Rule 4: Password must contain a special character and no whitespace.")
        return False


def hasUpper_reqs(s):
    # has an uppercase letter
    if any(char.isupper() for char in s):
        return True
    else:
        print("Rule 5: Password must contain an uppercase letter.")
        return False


def sixNine_reqs(s):
    digit_sum = sum(int(char) for char in s if char.isdigit())
    if digit_sum == 69:
        return True
    else:
        print("Rule 6: The digits in your password must add up to `69`.")
        return False


def dateToday_reqs(s):
    # turn datetime obj into string
    strToday = datetime.now().strftime("%Y-%m-%d")
    if strToday in s:
        return True
    else:
        print("Rule 7: Password must have the date today in `YYYY-MM-DD` format.")
        return False


def fetch_random_pokemon():
    global pokemonTypes, pokemonName
    pokeIndex = random.randrange(1, 1021)
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokeIndex}")

    if response.status_code == 200:
        pokemonData = response.json()
        pokemonName = pokemonData["name"].title()
        pokemonTypes = [type_data["type"]["name"] for type_data in pokemonData["types"]]
        pokemon_sprite_url = pokemonData["sprites"]["other"]["official-artwork"][
            "front_default"
        ]

        img = Image.open(requests.get(pokemon_sprite_url, stream=True).raw)
        img.show(title=pokemonName)
        print(
            f"Rule 8: A wild {pokemonName} appeared! Your password must include at least one of this Pokémon's type."
        )
        return pokemonTypes

    else:
        print(
            f"\nError: PokeAPI call failed. Error Code {response.status_code}. By default, get the type/s of Bulbasaur instead."
        )
        return ["grass", "poison"]


def reset_pokemon():
    global pokeCounter, pokemonTypes, pokemonName
    pokeCounter = 0
    pokemonTypes = fetch_random_pokemon()
    pokemonName = pokemonTypes[0]


def wildPokemon_reqs(s):
    global pokeCounter, pokemonTypes, pokemonName
    if pokemonTypes is None:
        fetch_random_pokemon()
        return False
    for type in pokemonTypes:
        if type not in s:
            pokeCounter += 1
            pokeCountdown = 3 - pokeCounter
            print(
                f"Rule 8: A wild {pokemonName} appeared! Your password must include at least one of this Pokémon's type.(Regenerates in {pokeCountdown} attempts)"
            )
            print(pokemonTypes)
            if pokeCounter == 3:
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
    global captcha, captchaCounter
    captchaCounter = 0
    captcha = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
    generate_audio_captcha()
    generate_image_captcha()


def captcha_reqs(s):
    global captcha, captchaCounter
    if captcha not in s:
        captchaCounter += 1
        captchaCountdown = 5 - captchaCounter
        print(
            f"Rule 9: Password must include the captcha in the `captcha.png`/`captcha.wav` in the same directory as this program. Regenerates in {captchaCountdown} attempts."
        )
        if captchaCounter == 5:
            print("Captcha reset!")
            reset_captcha()
        return False
    return True


def flag_reqs(s):
    with open("validFlag.txt") as file:
        list_validFlag = file.read().splitlines()

    # if s contains valid flag
    if any(char in s for char in list_validFlag):
        return True
    else:
        print(
            "Rule 10: Password must have the `flag emoji` of a country whose name/country code starts with the letter `P`."
        )
        return False


def month_reqs(s):
    strMonth = datetime.now().strftime("%B")
    if strMonth.casefold() in s.casefold():
        return True
    else:
        print("Rule 11: Password must include the `month` we're currently in.")
        return False


def food_reqs(s):
    # food item emoji list
    with open("validFood.txt") as file:
        list_validFood = file.read().splitlines()

    if any(char in s for char in list_validFood):
        return True
    else:
        print(
            "Rule 12: We've been here for so long… I'm hungry! Password must have a `food emoji`."
        )
        return False


def timeNow_reqs(s):
    strTime = datetime.now().strftime("%H:%M")
    if strTime.casefold() in s.casefold():
        return True
    else:
        print(
            "Rule 13: Your password must include the current time in `HH:MM` military time format."
        )
        return False


if __name__ == "__main__":
    captchaCounter = 0
    voice_dir = Path.cwd() / "en"
    captcha = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
    pokeCounter = 0
    pokemonTypes = None
    pokemonName = None
    generate_audio_captcha()
    generate_image_captcha()
    main()
