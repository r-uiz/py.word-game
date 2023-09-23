# py.word-game
My final project for Harvard's CS50 Python, heavily inspired by https://neal.fun/password-game/.
[[logs.md|See logs here]]
[[requirements.txt|See requirements here]]
## todo:
- [x] captcha code cleanup
- [x] make prettier
    - [x] banners for rules/notices
    - [x] delete old notices as to not spam terminal
- [x] add function documentation
- [ ] ~~add type hints~~
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
- [ ] add a visual for the timer in the time requirement for the confirm function (maybe a progress bar?)
- [ ] add functionality to disable colored text outputting (using argparse, for example)
- [ ] completely disable clipboard pasting in confirm function (Can just be pasted again if you have a clipboard manager)
- [ ] add funnier announcement at the end
- [ ] add more rules! [[README.md#addtl-rule-ideas|see below]]
    - Hopefully more that requires user to search for a solution (like the pokemon one) on the Internet like neal.fun's version. (Chess notation, Geoguessr, etc.)
    - Even more interactive ones.
- [ ] add a GUI for easier input and prettier overall. Check out: [tkinter](https://docs.python.org/3/library/tkinter.html) or [PyQt](https://riverbankcomputing.com/software/pyqt/intro)


## Addtl notes:
- `Rule 6: sixNine` and `Rule 13: HH:MM` requirements are quite the hassle later on (that's the point; should be a challenge) But I understand your struggle! (hell, imagine testing the code for yourself!); [this tool that I wrote](https://www.online-python.com/SEMPZn3TDb) (which is basically the `sixNine` requirement) would be useful just so editing attempts in real time would be less of a hassle since you'll be out of the terminal.

- Best to add the emojis in the beginning. It's a hassle to use the arrow keys when passing over country flags and other emoji since it modifies it visually and turns out your cursor is not at right spot. (I'm not sure if this is a problem with my terminal or the code itself, but it's a problem nonetheless)

- Emojis may not necessarily be 1 character, which will be confusing in the char limit functions.

### Addtl rule ideas:
- ~~Retype the valid password to confirm~~ added!
- ~~Retype the valid password backwards to confirm (will be hard with emojis)~~ added!
- ~~add numbers to captcha (fun lil challenge, bit of an annoyance but its a game, no?)~~ added!
- ~~lower max limit (might be too limiting)~~ configurable!
- include total length of password (will mess with current answers in int-based reqs)
- must include a palindrome that has a minimum of 5 characters and is not a number.
- With the given set of ten letters, must include a valid word that uses some of the letters given. Regenerates new set every time you get it wrong.(easier reset if impossible to make word)
- give broken code. add the solution
- randomly generate a chess board and ask for a best move (maybe use chess notation)
- randomly generate emoji set and ask for what movie it means (🚢🧊💔 = Titanic)
- Hmm... needs more RGB. Add emojis that are red, green, and blue. (🔴🟢🔵)
