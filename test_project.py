"""
Unit Tests for PywordGame Module

These tests covers only the validation methods of the PywordGame class.

Author: r._.uiz
"""
import pytest
import random
from datetime import datetime
from project import PywordGame  # Import the class to be tested


@pytest.fixture
def game_instance():
    return PywordGame()


def test_min_length_reqs(game_instance):
    """
    Test the min_length_reqs method.

    Note: The default minimum password length is 5 characters.
    """
    # Case 1: Password length is less than the minimum (should fail)
    password = "pass"
    assert not game_instance.min_length_reqs(password)

    # Case 2: Password length is exactly the minimum (should pass)
    password = "passw"
    assert game_instance.min_length_reqs(password)

    # Case 3: Password length is greater than the minimum (should pass)
    password = "password"
    assert game_instance.min_length_reqs(password)


def test_max_length_reqs(game_instance):
    """
    Test the max_length_reqs method.

    Note: The default maximum password length is 50 characters.
    """
    # Case 1: Password length is greater than the maximum (should fail)
    password = "VeryLongPassword1234567890123456789012345678901234567890"
    assert not game_instance.max_length_reqs(password)

    # Case 2: Password length is exactly the maximum (should pass)
    password = "VeryLongPassword1234567890123456789012345678901234"
    assert game_instance.max_length_reqs(password)

    # Case 3: Password length is less than the maximum (should pass)
    password = "Password"
    assert game_instance.max_length_reqs(password)


def test_has_number_reqs(game_instance):
    """
    Test the has_number_reqs method.
    """
    # Case 1: Password does not contain a number (should fail)
    password = "Password"
    assert not game_instance.has_number_reqs(password)

    # Case 2: Password contains a number (should pass)
    password = "Password1"
    assert game_instance.has_number_reqs(password)


def test_has_special_reqs(game_instance):
    """
    Test the has_special_reqs method.
    """
    # Case 1: Password does not contain a special character (should fail)
    password = "Password"
    assert not game_instance.has_special_reqs(password)

    # Case 2: Password contains a special character (should pass)
    password = "Password!"
    assert game_instance.has_special_reqs(password)


def test_has_upper_reqs(game_instance):
    """
    Test the has_upper_reqs method.
    """
    # Case 1: Password does not contain an uppercase letter (should fail)
    password = "password"
    assert not game_instance.has_upper_reqs(password)

    # Case 2: Password contains an uppercase letter (should pass)
    password = "Password"
    assert game_instance.has_upper_reqs(password)


def test_sum_reqs(game_instance):
    """
    Test the six_nine_reqs method.

    Note: Digits must add up to 69.
    """
    # Case 1: Password's digits do not add up to 69 (should fail)
    password = "Password1"
    assert not game_instance.sum_reqs(password)

    # Case 2: Password's digits add up to 69 (should pass)
    password = "Password99999996"
    assert game_instance.sum_reqs(password)


def test_date_today_reqs(game_instance):
    """
    Test the date_today_reqs method.

    Note: Date must be in YYYY-MM-DD format.
    """
    # Get today's date in YYYY-MM-DD format
    str_today = datetime.now().strftime("%Y-%m-%d")

    # Case 1: Password does not contain today's date (should fail)
    password = "Password"
    assert not game_instance.date_today_reqs(password)

    # Case 2: Password contains today's date (should pass)
    password = f"Password{str_today}"
    assert game_instance.date_today_reqs(password)

    pass


'''
Currently do not have the skill to make tests for these methods.
Will update this once I learn how to do it.

def test_wild_pokemon_reqs(game_instance):
    """
    Test the wild_pokemon_reqs method.
    """
    pokemon_type_list = [
        "Normal",
        "Fire",
        "Water",
        "Grass",
        "Electric",
        "Ice",
        "Fighting",
        "Poison",
        "Ground",
        "Flying",
        "Psychic",
        "Bug",
        "Rock",
        "Ghost",
        "Dark",
        "Dragon",
        "Steel",
        "Fairy",
    ]
    # Case 1: Password does not contain a valid pokemon type (should fail)
    password = "Password"
    assert not game_instance.wild_pokemon_reqs(password)

    # Case 2: Password contains a valid pokemon type (should pass)
    pokemon_type_random = random.choice(pokemon_type_list)
    password = f"Password{pokemon_type_random}"
    assert game_instance.wild_pokemon_reqs(password)


def test_captcha_reqs(game_instance):
    """
    Test the captcha_reqs method.
    """
    captcha = "".join(
        random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(5)
    )
    # Case 1: Password does not contain the captcha (should fail)
    password = "Password"
    assert not game_instance.captcha_reqs(password)

    # Case 2: Password contains the captcha (should pass)
    password = f"Password{captcha}"
    assert game_instance.captcha_reqs(password)

'''


def test_flag_reqs(game_instance):
    """
    Test the flag_reqs method.

    Note: Valid flags are in the validFlag.txt file.
    """
    # Case 1: Password does not contain valid flag (should fail)
    password = "Password"
    assert not game_instance.flag_reqs(password)

    # Case 2: Password contains valid flag (should pass)
    password = "Password🇵🇭"
    assert game_instance.flag_reqs(password)


def test_month_reqs(game_instance):
    """
    Test the month_reqs method.

    Note: Months must be in full name format.
    """
    # Get the current month in full name format
    str_month = datetime.now().strftime("%B")

    # Case 1: Password does not contain the current month (should fail)
    password = "Password"
    assert not game_instance.month_reqs(password)

    # Case 2: Password contains the current month (should pass)
    password = f"Password{str_month}"
    assert game_instance.month_reqs(password)


def test_food_reqs(game_instance):
    """
    Test the food_reqs method.

    Note: Valid foods are in the validFood.txt file.
    """
    # Case 1: Password does not contain a valid food (should fail)
    password = "Password"
    assert not game_instance.food_reqs(password)

    # Case 2: Password contains a valid food (should pass)
    password = "Password🍕"
    assert game_instance.food_reqs(password)


def test_time_now_reqs(game_instance):
    """
    Test the time_now_reqs method.

    Note: Time must be in HH:MM format.
    """
    # Get the current time in HH:MM format
    str_time = datetime.now().strftime("%H:%M")

    # Case 1: Password does not contain the current time (should fail)
    password = "Password"
    assert not game_instance.time_now_reqs(password)

    # Case 2: Password contains the current time (should pass)
    password = f"Password{str_time}"
    assert game_instance.time_now_reqs(password)
