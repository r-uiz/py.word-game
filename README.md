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
- [ ] add a visual for the timer in the time requirement


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
