# Polidoro Terminal
[![Upload Python Package](https://github.com/heitorpolidoro/polidoro-terminal/actions/workflows/python-publish.yml/badge.svg)](https://github.com/heitorpolidoro/polidoro-terminal/actions/workflows/python-publish.yml)
[![Lint with comments](https://github.com/heitorpolidoro/polidoro-terminal/actions/workflows/python-lint.yml/badge.svg)](https://github.com/heitorpolidoro/polidoro-terminal/actions/workflows/python-lint.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/heitorpolidoro/polidoro-terminal)
[![Coverage Status](https://coveralls.io/repos/github/heitorpolidoro/polidoro-terminal/badge.svg?branch=master)](https://coveralls.io/github/heitorpolidoro/polidoro-terminal?branch=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=heitorpolidoro_polidoro-terminal&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=heitorpolidoro_polidoro-terminal)

[![Latest](https://img.shields.io/github/release/heitorpolidoro/polidoro-terminal.svg?label=latest)](https://github.com/heitorpolidoro/polidoro-terminal/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/heitorpolidoro/polidoro-terminal)

![PyPI - Downloads](https://img.shields.io/pypi/dm/polidoro-terminal?label=PyPi%20Downloads)

![GitHub](https://img.shields.io/github/license/heitorpolidoro/polidoro-terminal)# py-terminal
### To install

```shell
sudo apt install python3-pip -y
pip3 install polidoro_terminal
```

### Terminal text formatting
Enums to help formatting text in terminal:
```python
from polidoro_terminal import Format
Format.NORMAL
Format.BOLD
Format.DIM
Format.UNDERLINE
Format.BLINK
Format.REVERSE
Format.STRIKE

from polidoro_terminal import Color
Color.BLACK
Color.RED
Color.GREEN
Color.YELLOW
Color.BLUE
Color.MAGENTA
Color.CYAN
Color.WHITE

Color.LIGHT_BLACK
Color.LIGHT_RED
Color.LIGHT_GREEN
Color.LIGHT_YELLOW
Color.LIGHT_BLUE
Color.LIGHT_MAGENTA
Color.LIGHT_CYAN
Color.LIGHT_WHITE

Color.BACKGROUND_BLACK
Color.BACKGROUND_RED
Color.BACKGROUND_GREEN
Color.BACKGROUND_YELLOW
Color.BACKGROUND_BLUE
Color.BACKGROUND_MAGENTA
Color.BACKGROUND_CYAN
Color.BACKGROUND_WHITE

Color.BACKGROUND_LIGHT_BLACK
Color.BACKGROUND_LIGHT_RED
Color.BACKGROUND_LIGHT_GREEN
Color.BACKGROUND_LIGHT_YELLOW
Color.BACKGROUND_LIGHT_BLUE
Color.BACKGROUND_LIGHT_MAGENTA
Color.BACKGROUND_LIGHT_CYAN
Color.BACKGROUND_LIGHT_WHITE
```
To use:

```python
from polidoro_terminal import Format, Color
print(f'{Color.CYAN}Hello{Format.NORMAL}')

print(f'{Color.RED + Format.BOLD}Error{Format.NORMAL}')
```

### Cursor

```python
from polidoro_terminal import cursor
cursor.hide()  # To hide the cursor
cursor.show()  # To show the cursor
```

### Getch

To read keys unblocked from keyboard
```python
from polidoro_terminal import getch

key = getch()

key = getch(translate_commands=True)  # Return if any special key is pressed
from polidoro_terminal import Key
Key.ENTER
Key.ESC
Key.ARROW_UP
Key.ARROW_DOWN
Key.ARROW_LEFT
Key.ARROW_RIGHT
Key.PAGE_UP
Key.PAGE_DOWN
Key.HOME
Key.END
Key.BACKSPACE
Key.INSERT
Key.DELETE
```

### Terminal manipulation

```python
from polidoro_terminal import clear_to_end_of_line, clear_to_end_of_screen, up_lines, move_left, move_right, erase_lines
clear_to_end_of_line()  # Clear from de cursor to end of line
clear_to_end_of_screen()  # Clear from cursor to end of screen
up_lines(N)  # Up N lines (default=1)
move_left(N)  # Move N characters to left (default=1)
move_right(N)  # Move N characters to right (default=1)
erase_lines(N)  # Erase N past lines (default=1)
```


### Terminal Size
```python
from polidoro_terminal import size, columns, rows

columns  # How many columns in the terminal window
rows  # How many rows in the terminal window
size #  columns, rows
```