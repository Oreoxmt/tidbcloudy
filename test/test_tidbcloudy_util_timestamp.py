from datetime import datetime, timezone

from tidbcloudy.util.timestamp import get_current_year_month, timestamp_to_string


def test_timestamp_to_string():
    assert timestamp_to_string(None) == ""
    assert timestamp_to_string(0, timezone=timezone.utc) == "1970-01-01 00:00:00"


def test_get_current_year_month():
    current_date = datetime.now(tz=timezone.utc)
    assert get_current_year_month(timezone=timezone.utc) == f"{current_date.year}-{current_date.month}"
