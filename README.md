# HW 3 R/Python Package

**Author**: Sheldon Yuan
**Date started**: November 13, 2026

## Description

This assignment creates a Python package `tennisplot`. This package retrieves a tennis player's career matches from [tennisabstract.com](https://www.tennisabstract.com) and plots them in the style of the New York Times graphic *"Serena Williams Dominated Her Generation, Then the Next One, Too"*.

Each dot represents one match, blue dots represent matches that the player won, and purple dots represent matches the player lost. The x-axis shows the player's age at the time of the match, the y-axis shows the age difference between them and their opponent.

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-2-sheldonyuan5.git
```
This also installs the two dependencies, `pandas` and `matplotlib` (>= 3.5). Requires Python >= 3.10.

## Usage

The package has two public functions:

| Function | Input | Output |
|---|---|---|
| `get_career_matches(player_name)` | a player's name | a clean data frame, one row per match |
| `plot_career_matches(career)` | the data frame from `get_career_matches()` | a matplotlib figure |

## Data Source

For a player such as Serena Williams, the package reads two files from tennisabstract.com:

- `jsmatches/SerenaWilliamsCareer.js` — every career match. Women's files
  store each opponent's **birth date**, so the opponent's age is computed;
  men's files store the opponent's **age** directly.
- `jsmatches/SerenaWilliams.js` — the player's profile, which contains the
  player's own birth date (`var dob=...`).

## Project File Structure

├── README.md
├── pyproject.toml # package metadata, dependencies, install settings
└── tennisplot/
├── init.py # version + the two public functions
├── data/
│ ├── init.py
│ └── get_career_data.py # get_career_matches() and its helpers
├── plot/
│ ├── init.py
│ └── plot_data.py # plot_career_matches() and its helpers
└── tests/
├── FemalePlayerCareer.JS # mockup female career file
├── MalePlayerCareer.JS # mockup male career file
└── test_get_career_data.py

## Personal Reflection

The biggest takeaway from finishing this project was how to split a complex function into various different, smaller ones. When writing the two functions, as I was borrowing much logic from the code I wrote last time for Homework 2, the code I initially wrote was in a very large chunk. The function being complicated and written in large pieces caused me to not be able to identify quickly what each part of the function does. However, after I saw the assignment requirement that "no function should be longer than 20 lines of code", I started breaking up the code I wrote for my functions, into various private functions that each help do a bit of the whole work. I found that this approach made the functions much more easily readable, bugs are also easier to find and identify. I will maintain this approach and request myself with this limit with future projects as well.
