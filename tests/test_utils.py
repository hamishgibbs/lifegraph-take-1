from compute.utils import parse_date
from datetime import datetime

class TestParseDate():

    def test_thepast(self):
        date = "thepast"
        res = parse_date(date)
        assert res == datetime(1, 1, 1, 0, 0)

    def test_thefuture(self):
        date = "thefuture"
        res = parse_date(date)
        assert res == datetime(9999, 12, 31, 23, 59, 59, 999999)

    def test_year(self):
        date = "2020"
        res = parse_date(date)
        assert res == datetime(2020, 1, 1, 0, 0)

    def test_date(self):
        date = "12-03-2020"
        res = parse_date(date)
        assert res == datetime(2020, 3, 12, 0, 0)

    def test_datetime(self):
        date = "12-03-2020 10:52:25"
        res = parse_date(date)
        assert res == datetime(2020, 3, 12, 10, 52, 25)
