# Terminarty 
###### A simple CLI helper for Python
[![License: MIT](https://img.shields.io/pypi/l/terminarty)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/terminarty)](https://pypi.org/project/terminarty/)
![Python versions](https://img.shields.io/pypi/pyversions/terminarty)

## Installation

```bash
$ pip install terminarty
```
## Features
**Inputs**
```python
from terminarty import Terminal

terminal = Terminal()

terminal.input("What is your name?")
```
!["What is yout name?"](https://imgur.com/huf4E5P.png)

**Choises**
```python
from terminarty import Choises

Choises.choise(["red", "green", "blue"], "What is your favorite color?")
```
!["What is your favorite color?" (red, green, blue)](https://imgur.com/NQwkfj6.png)

## And that is all?
**Yes.**