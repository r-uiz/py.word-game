# py.word-game
My final project for Harvard's CS50 Python, heavily inspired by https://neal.fun/password-game/.
[[logs.md|See logs here]]
[[requirements.txt|See requirements here]]
## todo:
- [x] captcha code cleanup
- [ ] make prettier
    - [ ] banners for rules/notices
    - [ ] delete old notices as to not spam terminal
- [ ] add function documentation
- [ ] add type hints
- [ ] create test file
- [ ] finalize readme
    - [ ] explain program
        - [ ] rules/requirements
    - [ ] explain imported libraries
    - [ ] explain dependencies
    - [ ] what could be done better (input, mainly; clunky clipboard)
    - [ ] add logs
- [ ] submit!

## someday:
- [ ] add a GUI for easier input and prettier overall. Check out: [tkinter](https://docs.python.org/3/library/tkinter.html) or [PyQt](https://riverbankcomputing.com/software/pyqt/intro)


## Addtl notes:
- `Rule 6: sixNine` and `Rule 13: HH:MM` requirements are quite the hassle later on (that's the point; should be a challenge) But I understand your struggle! (hell, imagine testing the code for yourself!); [this tool that I wrote](https://www.online-python.com/SEMPZn3TDb) (which is basically the `sixNine` requirement) would be useful just so editing attempts in real time would be less of a hassle since you'll be out of the terminal.

- Best to add the emojis in the beginning. It's a hassle to use the arrow keys when passing over country flags and other emoji since it modifies it visually and turns out your cursor is not at right spot. (I'm not sure if this is a problem with my terminal or the code itself, but it's a problem nonetheless)

- Emojis may not necessarily be 1 character, which will be confusing in the char limit functions.

### Addtl rule ideas:
- Retype the valid password to confirm
- Retype the valid password backwards to confirm (will be hard with emojis)
    - not running time func
- add numbers to captcha (fun lil challenge, bit of an annoyance but its a game, no?)
- lower max limit (might be too limiting)
- include total length of password (will mess with current answers in int-based reqs)
- must include a palindrome that has a minimum of 5 characters and is not a number.
- With the given set of ten letters, must include a valid word that uses some of the letters given. Regenerates new set every time you get it wrong.(easier reset if impossible to make word)


## Things to improve as per ChatGPT:
Your code is well-structured and follows good practices. However, there are always opportunities for improvement and enhancements. Here are some suggestions to further improve your code:

1. **Function Documentation**: Consider adding docstrings to your functions to provide clear explanations of what each function does. This can help other developers (and your future self) understand the purpose of each function.

```python
def minLength_reqs(s):
    """
    Check if the password meets the minimum length requirement.

    Args:
        s (str): The password to check.

    Returns:
        bool: True if the password meets the requirement, False otherwise.
    """
    # Function code here
```

2. **Consistent Naming**: Ensure consistent naming conventions. For example, you use both `camelCase` and `snake_case` for variable names. Stick to one convention throughout your code for clarity.

3. **Error Handling**: Add more detailed error handling for requests to the PokeAPI or other external services. Currently, if there's an error, it prints a message but doesn't provide much information about the problem. You can log the error details or raise exceptions to handle errors more gracefully.

4. **Separate Configuration**: Consider moving configuration settings, such as the maximum password length and the default values for Pokémon types, into separate constants at the beginning of your script. This makes it easier to change these values in the future.

5. **Modularization**: Depending on your future plans for the code, you might consider splitting it into multiple files or classes. This can make it easier to manage and test various components independently.

6. **Unit Tests**: Write unit tests for your validation functions. This will help ensure that each validation rule works as expected and makes it easier to catch issues as your code evolves.

7. **Use Constants for Magic Values**: Instead of hardcoding values like `69` or the number `5`, use constants with meaningful names. This improves code readability and maintainability.

8. **Improve User Instructions**: Provide more user-friendly instructions for each rule, including examples if possible, to make it easier for users to understand the requirements.

9. **Error Messages**: Consider formatting error messages consistently and providing clear guidance on what went wrong and how to fix it.

10. **Logging**: Use the Python `logging` module for logging messages and errors. This allows you to control the log level and easily switch between displaying messages and saving them to a log file.

11. **Use f-strings**: You've already used f-strings in some places, but you can use them consistently throughout your code for string formatting, which is more readable and concise.

12. **Use Function Defaults**: For some of your functions, you can utilize default function arguments instead of global variables. For example, in `wildPokemon_reqs`, you can set default values for `pokeCounter`, `pokemonTypes`, and `pokemonName`.

13. **Consider User Experience**: Think about the overall user experience. Are there any improvements you can make to the user interface to make it more intuitive or informative?

These suggestions should help you further improve your code's readability, maintainability, and functionality. However, remember that code improvement is an iterative process, and you can always come back to refine it further as you gain more experience and requirements change.