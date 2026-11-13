import json
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import pandas as pd

BASE_URL = "https://www.tennisabstract.com"
DAYS_PER_YEAR = 365.25
DATE = 0
RESULT = 4
OPPONENT_INFO = 16  
RESULT_LABELS = {"W": "Won", "L": "Lost"}
NOT_FOUND_MESSAGE = ("No player named '{}' found on tennisabstract.com (HTTP {}). "
                     "Please check the spelling and try again.")

def get_career_matches(player_name):
    url_name = _format_name(player_name)
    career_url = f"{BASE_URL}/jsmatches/{url_name}Career.js"
    profile_url = f"{BASE_URL}/jsmatches/{url_name}.js"
    matches = _parse_matches(_download_text(career_url, player_name))
    birth_date = _parse_birth_date(_download_text(profile_url, player_name))
    return _build_table(matches, birth_date, _display_name(url_name))

def _format_name(player_name):
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("player_name must be a non-empty string, e.g. 'Serena Williams'")
    return "".join(word[0].upper() + word[1:] for word in player_name.split())

def _display_name(url_name):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", url_name)

def _download_text(url, player_name):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request) as response:
            return response.read().decode("utf-8", errors="replace")
    except HTTPError as error:
        raise ValueError(NOT_FOUND_MESSAGE.format(player_name, error.code)) from None

def _parse_matches(career_text):
    start, end = career_text.index("["), career_text.rindex("]") + 1
    return json.loads(career_text[start:end])

def _is_female(matches):
    first_value = matches[0][OPPONENT_INFO]
    return len(first_value) == 8 and first_value.isdigit()

def _parse_birth_date(profile_text):
    found = re.search(r"var dob\s*=\s*(\d{8})", profile_text)
    if found is None:
        raise ValueError("Could not find the player's birth date on tennisabstract.com")
    return pd.to_datetime(found.group(1), format="%Y%m%d")

def _build_table(matches, birth_date, player):
    career = pd.DataFrame({
        "date": pd.to_datetime([match[DATE] for match in matches], format="%Y%m%d"),
        "result": [RESULT_LABELS.get(match[RESULT]) for match in matches],
    })
    career = _add_ages(career, matches, birth_date)
    career.insert(0, "player", player)
    return career.sort_values("date", ignore_index=True)

def _add_ages(career, matches, birth_date):
    career["player_age"] = _years_between(birth_date, career["date"])
    career["opponent_age"] = _opponent_ages(matches, career["date"])
    career["age_difference"] = (career["player_age"] - career["opponent_age"]).round(3)
    return career

def _opponent_ages(matches, dates):
    values = pd.Series([match[OPPONENT_INFO] for match in matches])
    if _is_female(matches):
        birth_dates = pd.to_datetime(values, format="%Y%m%d", errors="coerce")
        return _years_between(birth_dates, dates)
    return pd.to_numeric(values, errors="coerce").round(3)

def _years_between(earlier, later):
    return ((later - earlier).dt.days / DAYS_PER_YEAR).round(3)
    