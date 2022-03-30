from compute.utils import (
    parse_date,
    daterange_includes_now
)
from astropy.time import Time

class TestParseDate():

    def test_thepast(self):
        date = "thepast"
        res = parse_date(date)
        assert res == Time(f"-{4713:05}-01-01T00:00:00", format="fits")

    def test_thefuture(self):
        date = "thefuture"
        res = parse_date(date)
        assert res == Time.strptime("9999", "%Y")

    def test_year_bc(self):
        date = "520 BC"
        res = parse_date(date)
        assert res == Time(f"-{520:05}-01-01T00:00:00", format="fits")

    def test_year_ad(self):
        date = "520 AD"
        res = parse_date(date)
        assert res == Time(f"{520:04}-01-01T00:00:00", format="fits")

    def test_year(self):
        date = "2020"
        res = parse_date(date)
        assert res == Time.strptime("1-1-2020 00:00:00", "%d-%m-%Y %H:%M:%S")

    def test_date(self):
        date = "12-03-2020"
        res = parse_date(date)
        assert res == Time.strptime("12-3-2020 00:00:00", "%d-%m-%Y %H:%M:%S")

    def test_datetime(self):
        date = "12-03-2020 10:52:25"
        res = parse_date(date)
        assert res == Time.strptime("12-3-2020 10:52:25", "%d-%m-%Y %H:%M:%S")

def test_daterange_includes_now_true():
    start = parse_date("thepast")
    end = parse_date("thefuture")
    res = daterange_includes_now(start, end)
    assert res

def test_daterange_includes_now_false():
    start = parse_date("1970")
    end = parse_date("1985")
    res = daterange_includes_now(start, end)
    assert not res
