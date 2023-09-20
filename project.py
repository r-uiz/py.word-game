import re
import sys
import string
import random
import subprocess
from datetime import datetime
from captcha.image import ImageCaptcha


def main():
    # explanation
    print("Welcome to Py.word Game! Choose a password.")
    print("Ctrl+C to quit the program")
    # ask for attempt
    try:
        while True:
            attempt = input("Password: ")
            if validate(attempt) == False:
                subprocess.run("pbcopy", text=True, input=attempt)
                print("Last attempt copied to clipboard. Ctrl+C to quit.")
                pass
            else:
                sys.exit(
                    f'Congrats! Password "{attempt}" is valid. Wait... did we say that out loud?'
                )
    except KeyboardInterrupt:
        print("\nProgram quit. Try to create a password again later!")


def validate(s):
    if (
        normal_reqs(s) == True
        and sixnine_reqs(s) == True
        and datetoday_reqs(s) == True
        and pokemonmove_reqs(s) == True
        and captcha_reqs(s) == True
        and flag_reqs(s) == True
        and month_reqs(s) == True
        and food_reqs(s) == True
        and timenow_reqs(s) == True
    ):
        # passes all requirements
        return True
    else:
        # invalid password
        return False


def normal_reqs(s):
    # string of if statements; if all pass, return True.
    # grouped together because quite normal requirements
    # 5 - 50 char limit; len()
    # include a number; any() str.isdigit()
    # has a special char and no whitespace; not isalnum, not " " in attempt
    # has an uppercase letter; any(), isupper for char in attempt
    return True


def sixnine_reqs(s):
    # get all digits sum, if 69 return True; for loop, isdigit
    return True


def datetoday_reqs(s):
    # get date today with datetime
    # turn into string
    # put in variable
    # if today in str
    return True


def pokemonmove_reqs(s):
    # api call
    # get list of moves
    # if in s, True
    return True


def captcha_reqs(s):
    # attempt counter; if div by 5,
    # regenerate captcha with random
    # captcha = ImageCaptcha()
    return True


def flag_reqs(s):
    # valid flags list
    # if s contains valid flag
    return True


def month_reqs(s):
    # get current month with datetime
    # turn into string
    # put in variable
    # if month in str
    return True


def food_reqs(s):
    # food emoji list
    # if s contains food, True
    return True


def timenow_reqs(s):
    # get current time with datetime
    # turn into string
    # put in variable
    # if time in str
    return True


if __name__ == "__main__":
    main()
