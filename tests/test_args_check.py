import pytest
from datetime import datetime
from my_module import ArgsCheck


class TestArgsCheck:
    @staticmethod
    def test_date_check():
        # Test valid dates
        assert ArgsCheck.date_check("20210101", "20211231") == 1

        # Test invalid dates
        with pytest.raises(SystemExit):
            ArgsCheck.date_check("20220101", "20220102")  # start date in the future
        with pytest.raises(SystemExit):
            ArgsCheck.date_check("20200101", "20201231")  # end date in the past
        with pytest.raises(SystemExit):
            ArgsCheck.date_check("203/20/299", "203/22/299")  # invalid date format
        with pytest.raises(SystemExit):
            ArgsCheck.date_check("100/01/01", "500/01/01")  # dates out of bounds
        with pytest.raises(SystemExit):
            ArgsCheck.date_check("20220101", "20231231")  # no trading days found

    @staticmethod
    def test_aum_check():
        # Test valid AUM
        assert ArgsCheck.aum_check(100000) is None

        # Test invalid AUM
        with pytest.raises(SystemExit):
            ArgsCheck.aum_check(0)  # AUM must be greater than 0
        with pytest.raises(SystemExit):
            ArgsCheck.aum_check(-5000)  # AUM must be greater than 0

    @staticmethod
    def test_strategy_check():
        # Test valid strategy
        assert ArgsCheck.strategy_check("M") is None
        assert ArgsCheck.strategy_check("R") is None

        # Test invalid strategy
        with pytest.raises(SystemExit):
            ArgsCheck.strategy_check("C")  # invalid strategy
