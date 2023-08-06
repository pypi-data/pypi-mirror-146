# test framework
import unittest
import pytest

# package
from caellion.pycommons.stringutil.formatters import NumberFormatting as fmt
from caellion.pycommons.stringutil.formatters import InvalidDurationException


# test cases
class TestStringUtilFormatters:
    # SI formatter
    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "0"),
            (0, 3, "0.000"),
            (1000, 0, "1k"),
            (1000000, 0, "1M"),
            (123.456, 3, "123.456"),
            (1234.56, 3, "1.235k"),
            (123456, 3, "123.456k"),
            (123456789, 3, "123.457M"),
            (999999, 3, "999.999k"),
            (12345678901234567890123456789, 0, "12346Y"),
            (12345678901234567890123456789000, 0, "12345679Y"),
        ],
    )
    def test_fmt_si_plus(self, value, decimals, expected):
        assert fmt.formatSI(value, decimals) == expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            (0, "0"),
            (1000, "1k"),
            (1000000, "1M"),
            (12345678901234567890123456789, "12346Y"),
        ],
    )
    def test_fmt_si_plus_no_decimals(self, value, expected):
        assert fmt.formatSI(value) == expected

    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "0"),
            (0, 3, "0.000"),
            (-1000, 0, "-1k"),
            (-1000000, 0, "-1M"),
            (-123.456, 3, "-123.456"),
            (-1234.56, 3, "-1.235k"),
            (-123456, 3, "-123.456k"),
            (-123456789, 3, "-123.457M"),
            (-999999, 3, "-999.999k"),
            (-12345678901234567890123456789, 0, "-12346Y"),
        ],
    )
    def test_fmt_si_minus(self, value, decimals, expected):
        assert fmt.formatSI(value, decimals) == expected

    # binary SI
    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "0"),
            (1024, 0, "1ki"),
            (1024 * 1024, 0, "1Mi"),
            (512 * 1024, 3, "512.000ki"),
            (256520, 0, "251ki"),
            (256520, 3, "250.508ki"),
            (10240002, 3, "9.766Mi"),
            (12345678901234567890123456789, 0, "10212Yi"),
        ],
    )
    def test_fmt_si_bin_plus(self, value, decimals, expected):
        assert fmt.formatBinarySI(value, decimals) == expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            (0, "0"),
            (1024, "1ki"),
            (1024 * 1024, "1Mi"),
            (256520, "251ki"),
            (12345678901234567890123456789, "10212Yi"),
        ],
    )
    def test_fmt_si_bin_plus_no_decimals(self, value, expected):
        assert fmt.formatBinarySI(value) == expected

    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "0"),
            (-1024, 0, "-1ki"),
            (-1024 * 1024, 0, "-1Mi"),
            (-512 * 1024, 3, "-512.000ki"),
            (-256520, 0, "-251ki"),
            (-256520, 3, "-250.508ki"),
            (-10240002, 3, "-9.766Mi"),
            (-12345678901234567890123456789, 0, "-10212Yi"),
        ],
    )
    def test_fmt_si_bin_minus(self, value, decimals, expected):
        assert fmt.formatBinarySI(value, decimals) == expected

    # subvalues
    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "0"),
            (0, 3, "0.000"),
            (0.100, 0, "100m"),
            (0.000100, 0, "100μ"),
            (0.000000100, 0, "100n"),
            (0.0001231, 1, "123.1μ"),
            (0.135100, 0, "135m"),
            (1e-50, 0, "0y"),
            (1e-24, 0, "1y"),
            (1e-25, 0, "0y"),
            (9.999e-25, 0, "0y"),
        ],
    )
    def test_fmt_si_sub_plus(self, value, decimals, expected):
        assert fmt.formatSISubValue(value, decimals) == expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            (0, "0"),
            (0.100, "100m"),
            (0.000100, "100μ"),
            (0.000000100, "100n"),
            (0.135100, "135m"),
            (1e-50, "0y"),
        ],
    )
    def test_fmt_si_sub_plus_no_decimals(self, value, expected):
        assert fmt.formatSISubValue(value) == expected

    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "0"),
            (0, 3, "0.000"),
            (-0.100, 0, "-100m"),
            (-0.000100, 0, "-100μ"),
            (-0.000000100, 0, "-100n"),
            (-0.0001231, 1, "-123.1μ"),
            (-0.135100, 0, "-135m"),
            (-1e-50, 0, "-0y"),
        ],
    )
    def test_fmt_si_sub_minus(self, value, decimals, expected):
        assert fmt.formatSISubValue(value, decimals) == expected

    # subvalues
    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "BinSubValueError"),
            (0, 3, "BinSubValueError"),
            (0.100, 0, "BinSubValueError"),
            (0.000100, 0, "BinSubValueError"),
            (0.000000100, 0, "BinSubValueError"),
            (0.0001231, 1, "BinSubValueError"),
            (0.135100, 0, "BinSubValueError"),
            (1e-50, 0, "BinSubValueError"),
        ],
    )
    def test_fmt_si_binary_sub_plus(self, value, decimals, expected):
        assert fmt.formatSIBinarySubValue(value, decimals) == expected

    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "BinSubValueError"),
            (0, 3, "BinSubValueError"),
            (-0.100, 0, "BinSubValueError"),
            (-0.000100, 0, "BinSubValueError"),
            (-0.000000100, 0, "BinSubValueError"),
            (-0.0001231, 1, "BinSubValueError"),
            (-0.135100, 0, "BinSubValueError"),
            (-1e-50, 0, "BinSubValueError"),
        ],
    )
    def test_fmt_si_binary_sub_minus(self, value, decimals, expected):
        assert fmt.formatSIBinarySubValue(value, decimals) == expected

    # full-range formatters
    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "0"),
            (0, 3, "0.000"),
            (1000, 0, "1k"),
            (1000000, 0, "1M"),
            (123.456, 3, "123.456"),
            (1234.56, 3, "1.235k"),
            (123456, 3, "123.456k"),
            (123456789, 3, "123.457M"),
            (999999, 3, "999.999k"),
            (12345678901234567890123456789, 0, "12346Y"),
            (0.100, 0, "100m"),
            (0.000100, 0, "100μ"),
            (0.000000100, 0, "100n"),
            (0.0001231, 1, "123.1μ"),
            (0.135100, 0, "135m"),
            (1e-50, 0, "0y"),
            (1, 0, "1"),
            (1 - 1e-24, 0, "1"),
        ],
    )
    def test_fmt_si_plus_fullrange(self, value, decimals, expected):
        assert fmt.formatSIFullRange(value, decimals) == expected

    @pytest.mark.parametrize(
        "value,decimals,expected",
        [
            (0, 0, "0"),
            (0, 3, "0.000"),
            (-1000, 0, "-1k"),
            (-1000000, 0, "-1M"),
            (-123.456, 3, "-123.456"),
            (-1234.56, 3, "-1.235k"),
            (-123456, 3, "-123.456k"),
            (-123456789, 3, "-123.457M"),
            (-999999, 3, "-999.999k"),
            (-12345678901234567890123456789, 0, "-12346Y"),
            (0.100, 0, "100m"),
            (0.000100, 0, "100μ"),
            (0.000000100, 0, "100n"),
            (0.0001231, 1, "123.1μ"),
            (0.135100, 0, "135m"),
            (-1e-50, 0, "-0y"),
            (-1, 0, "-1"),
            (-1 + 1e-24, 0, "-1"),
        ],
    )
    def test_fmt_si_minus_fullrange(self, value, decimals, expected):
        assert fmt.formatSIFullRange(value, decimals) == expected

    @pytest.mark.parametrize(
        "units,seconds,unit,expected",
        [
            (9.99, 365000 * 86400, "unit", "9.99unit/millennium"),
            (1.0, 365000 * 86400, "unit", "1.00unit/millennium"),
            (9.99, 36500 * 86400, "unit", "9.99unit/century"),
            (1.0, 36500 * 86400, "unit", "1.00unit/century"),
            (9.99, 365 * 86400, "unit", "9.99unit/year"),
            (1.0, 365 * 86400, "unit", "1.00unit/year"),
            (6.99, 7 * 86400.0, "unit", "6.99unit/week"),
            (1.0, 7 * 86400.0, "unit", "1.00unit/week"),
            (9.99, 86400.0, "unit", "9.99unit/day"),
            (1.0, 86400.0, "unit", "1.00unit/day"),
            (9.99, 3600.0, "unit", "9.99unit/hour"),
            (1.0, 3600.0, "unit", "1.00unit/hour"),
            (1.0, 60.0, "unit", "1.00unit/minute"),
            (1.0, 1.0, "unit", "1.00unit/second"),
            (0.0, 1.0, "unit", "0.00unit/millennium"),
            (1.0, 0.001, "unit", "1.00unit/millisecond"),
            (1.0, 0.000001, "unit", "1.00unit/microsecond"),
            (-1.0, 0.000001, "unit", "-1.00unit/microsecond"),
        ],
    )
    def test_fmt_units_per_interval(self, units, seconds, unit, expected):
        assert fmt.formatUnitsPerIntervalDynamic(
            units, seconds, unit) == expected

    @pytest.mark.parametrize(
        "units,seconds,unit", [(1.0, -0.000001, "unit"), (1.0, 0, "unit")]
    )
    def test_fmt_units_per_interval_negative_duration_exception(
        self, units, seconds, unit
    ):
        with pytest.raises(InvalidDurationException):
            fmt.formatUnitsPerIntervalDynamic(units, seconds, unit)


if __name__ == "__main__":
    unittest.main()
