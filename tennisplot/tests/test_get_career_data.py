from pathlib import Path

import pandas as pd
import pytest

from tennisplot.data.get_career_data import (_build_table, _format_name, _is_female, _parse_birth_date, _parse_matches,)

TEST_DIR = Path(__file__).parent
COLUMNS = ["player", "date", "result", "player_age", "opponent_age", "age_difference"]

def _read_matches(filename):
    return _parse_matches((TEST_DIR / filename).read_text())

def _female_table():
    return _build_table(_read_matches("FemalePlayerCareer.JS"), pd.Timestamp("1981-09-26"), "Serena Williams")

def _male_table():
    return _build_table(_read_matches("MalePlayerCareer.JS"), pd.Timestamp("1986-06-03"), "Rafael Nadal")

def test_parse_matches_reads_every_row():
    assert len(_read_matches("FemalePlayerCareer.JS")) == 3
    assert len(_read_matches("MalePlayerCareer.JS")) == 3

def test_parse_matches_keeps_fields():
    first = _read_matches("FemalePlayerCareer.JS")[0]
    assert first[0] == "19951030"
    assert first[11] == "Anne Miller"
    assert first[16] == "19770119"

def test_is_female_detects_file_type():
    assert _is_female(_read_matches("FemalePlayerCareer.JS"))
    assert not _is_female(_read_matches("MalePlayerCareer.JS"))

def test_table_has_expected_columns():
    assert list(_female_table().columns) == COLUMNS
    assert list(_male_table().columns) == COLUMNS

def test_female_opponent_age_from_birth_date():
    first = _female_table().iloc[0]
    assert first["player_age"] == pytest.approx(14.092)
    assert first["opponent_age"] == pytest.approx(18.776)
    assert first["age_difference"] == pytest.approx(-4.684)

def test_male_opponent_age_read_directly():
    first = _male_table().iloc[0]
    assert first["player_age"] == pytest.approx(15.272)
    assert first["opponent_age"] == pytest.approx(22.264)
    assert first["age_difference"] == pytest.approx(-6.992)

def test_results_are_labeled():
    assert set(_female_table()["result"]) == {"Lost"}
    assert set(_male_table()["result"]) == {"Won", "Lost"}

def test_rows_sorted_by_date():
    assert _female_table()["date"].is_monotonic_increasing
    assert _male_table()["date"].is_monotonic_increasing

def test_no_missing_values():
    assert not _female_table().isna().any().any()
    assert not _male_table().isna().any().any()

@pytest.mark.parametrize("name", ["serena williams", "Serena Williams", "SerenaWilliams"])
def test_format_name_accepts_variants(name):
    assert _format_name(name) == "SerenaWilliams"

def test_format_name_rejects_empty():
    with pytest.raises(ValueError):
        _format_name("   ")

def test_parse_birth_date_finds_dob():
    assert _parse_birth_date("var dob=19810926;") == pd.Timestamp("1981-09-26")
    assert _parse_birth_date("var dob = 19860603;") == pd.Timestamp("1986-06-03")

def test_parse_birth_date_missing_raises():
    with pytest.raises(ValueError):
        _parse_birth_date('var dob_approx="";')
        