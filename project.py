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

    # if finally valid, exit


def validate(s):
    # contains all reqs; para prettier main lang
    # if invalid based on req, return False.
    # if valid, return True
    return False


def normal_reqs(s):
    # string of if statements; if all pass, return True.
    # grouped together because quite normal requirements
    # 5 - 50 char limit; len()
    # include a number; any() str.isdigit()
    # has a special char and no whitespace; not isalnum, not " " in attempt
    # has an uppercase letter; any(), isupper for char in attempt
    ...


def sixnine_reqs(s):
    # get all digits sum, if 69 return True; for loop, isdigit
    ...


def datetoday_reqs(s):
    # get date today with datetime
    # turn into string
    # put in variable
    # if today in str

    ...


def pokemonmove_reqs(s):
    # api call
    # get list of moves
    # if in s, True
    ...


def captcha_reqs(s):
    # attempt counter; if div by 5,
    # regenerate captcha with random
    captcha = ImageCaptcha()
    ...


def flag_reqs(s):
    # valid flags list
    # if s contains valid flag
    ...


def month_reqs(s):
    # get current month with datetime
    # turn into string
    # put in variable
    # if month in str
    ...


def food_reqs(s):
    # food emoji list
    # if s contains food, True
    ...


def timenow_reqs(s):
    # get current time with datetime
    # turn into string
    # put in variable
    # if time in str
    ...


if __name__ == "__main__":
    main()
