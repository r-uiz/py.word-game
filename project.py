import re
import sys
import string
import random
import readline
import subprocess
from datetime import datetime
from io import BytesIO
from pathlib import Path, PurePath
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha


def main():
    # explanation
    print("Welcome to Py.word Game! Choose a password.")
    print("Ctrl+C to quit the program")
    # ask for attempt
    try:
        while True:
            attempt = input("Password: ")
            if validate(attempt.strip()) == False:
                print(
                    "Last attempt copied to clipboard. Attempt again or Ctrl+C to quit."
                )
                pass
            else:
                sys.exit(
                    f'Congrats! Password "{attempt}" is valid. Wait... did we say that out loud?'
                )
    except KeyboardInterrupt:
        print("\nProgram quit. Try to create a password again later!")


def validate(s):
    if (
        minLength_reqs(s) == True
        and maxLength_reqs(s) == True
        and hasNumber_reqs(s) == True
        and hasSpecial_reqs(s) == True
        and hasUpper_reqs(s) == True
        and sixNine_reqs(s) == True
        and dateToday_reqs(s) == True
        and pokemonMove_reqs(s) == True
        and captcha_reqs(s) == True
        and flag_reqs(s) == True
        and month_reqs(s) == True
        and food_reqs(s) == True
        and timeNow_reqs(s) == True
    ):
        # passes all requirements
        return True
    else:
        # invalid password
        # copies last attempt to your clipboard
        subprocess.run("pbcopy", text=True, input=s)
        return False


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
    if (
        # has a special char
        any(char in specialCharacters for char in s)
        # does not have whitespace
        and bool(re.findall(r"[ ]+", s)) == False
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
    sum = 0
    for char in s:
        # add to sum if digit
        if char.isdigit() == True:
            x = int(char)
            sum += x
    if sum == 69:
        return True
    else:
        print("Rule 6: The digits in your password must add up to `69`.")
        return False


def dateToday_reqs(s):
    now = datetime.now()
    # turn datetime obj into string
    strToday = now.strftime("%Y-%m-%d")
    if strToday in s:
        return True
    else:
        print("Rule 7: Password must have the date today in `YYYY-MM-DD` format.")
        return False


def pokemonMove_reqs(s):
    # api call
    # get list of moves
    # if in s, True
    return True


def captcha_reqs(s):
    ...
    return True


def flag_reqs(s):
    with open("validFlag.txt") as file:
        list_validFlag = file.read().splitlines()

    # if s contains valid flag
    if any(char in s for char in list_validFlag):
        return True
    else:
        print("Rule 10: Password must have the `flag emoji` of a country whose name/country code starts with the letter `P`.")
        return False


def month_reqs(s):
    now = datetime.now()
    # turn datetime obj's month into full string
    strMonth = now.strftime("%B")
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
        print("Rule 12: We've been here for so long… I'm hungry! Password must have a `food emoji`.")
        return False


def timeNow_reqs(s):
    now = datetime.now()
    # turn datetime obj's HH:MM into string
    strTime = now.strftime("%H:%M")
    if strTime.casefold() in s.casefold():
        return True
    else:
        print("Rule 13: Your password must include the current time in `HH:MM` military time format.")
        return False


if __name__ == "__main__":
    main()
