# test framework
import unittest
import pytest

# package
from caellion.pycommons.stringutil.unixpassword import UnixPasswordText as upt
from caellion.pycommons.stringutil.unixpassword import NewlineEmptyException
from caellion.pycommons.stringutil.unixpassword import DuplicateFieldException
from caellion.pycommons.stringutil.unixpassword import EmptyFieldNameException
from caellion.pycommons.stringutil.unixpassword import SeparatorEmptyException
from caellion.pycommons.stringutil.unixpassword import InvalidFileFormatException


# test cases
class TestStringUtilUnixPasswordText:
    # @params((0, 0, "0"), (0, 3, "0.000"), (1000, 0, "1k"), (1000000, 0, "1M"), (123.456, 3, "123.456"), (1234.56, 3, "1.235k"), (123456, 3, "123.456k"), (123456789, 3, "123.457M"), (999999, 3, "999.999k"), (12345678901234567890123456789, 0, "12346Y"), (12345678901234567890123456789000, 0, "12345679Y"))
    # def test_fmt_si_plus(self, value, decimals, expected):
    #     assert (fmt.formatSI(value, decimals), expected)

    def test_upt_duplicate_keynames(self):
        with pytest.raises(DuplicateFieldException):
            upto = upt(["a", "b", "a"], ":", "\n")  # noqa

    def test_upt_empty_keyname(self):
        with pytest.raises(EmptyFieldNameException):
            upto = upt(["a", "", "a"], ":", "\n")  # noqa

    def test_upt_none_keyname(self):
        with pytest.raises(EmptyFieldNameException):
            upto = upt(["a", None, "a"], ":", "\n")  # noqa

    def test_upt_empty_separator(self):
        with pytest.raises(SeparatorEmptyException):
            upto = upt(["a", "b", "c"], "", "\n")  # noqa

    def test_upt_none_separator(self):
        with pytest.raises(SeparatorEmptyException):
            upto = upt(["a", "b", "c"], None, "\n")  # noqa

    def test_upt_empty_newline(self):
        with pytest.raises(NewlineEmptyException):
            upto = upt(["a", "b", "c"], ":", "")  # noqa

    def test_upt_none_newline(self):
        with pytest.raises(NewlineEmptyException):
            upto = upt(["a", "b", "c"], ":", None)  # noqa

    def test_upt_invalid_line(self):
        with pytest.raises(InvalidFileFormatException):
            upto = upt(["a", "b", "c"], ":", "\n")  # noqa
            upto.add_line_from_text("a:b:c:d")

    def test_upt_invalid_block(self):
        with pytest.raises(InvalidFileFormatException):
            upto = upt(["a", "b", "c"], ":", "\n")  # noqa
            upto.load_text("a:b:c\nd:e:f\ng:h:i\ny:\na:b:d:c")

    @pytest.mark.parametrize(
        "arg,expected",
        [
            ("1:1:1", {"a": "1", "b": "1", "c": "1"}),
            ("1:2:3", {"a": "1", "b": "2", "c": "3"}),
            ("a:b:c", {"a": "a", "b": "b", "c": "c"}),
            ("f:e:d", {"a": "f", "b": "e", "c": "d"}),
            (
                "some longer string:with more data:exe",
                {"a": "some longer string", "b": "with more data", "c": "exe"},
            ),
        ],
    )
    def test_upt_parse_line_ok(self, arg, expected):
        a = upt(["a", "b", "c"])
        result = a.parse_line(arg)
        assert result == expected

    @pytest.mark.parametrize(
        "arg,expected",
        [
            ({"a": "1", "b": "1", "c": "1"}, "1:1:1"),
            ({"a": "1", "b": "2", "c": "3"}, "1:2:3"),
            ({"a": "a", "b": "b", "c": "c"}, "a:b:c"),
            ({"a": "f", "b": "e", "c": "d"}, "f:e:d"),
            (
                {"a": "some longer string", "b": "with more data", "c": "exe"},
                "some longer string:with more data:exe",
            ),
        ],
    )
    def test_upt_create_line_ok(self, arg, expected):
        a = upt(["a", "b", "c"])
        result = a.create_line(arg)
        assert result == expected

    @pytest.mark.parametrize(
        "arg",
        [
            ({"a": "1", "b": "1", "c": "1"}),
            ({"a": "1", "b": "2", "c": "3"}),
            ({"a": "a", "b": "b", "c": "c"}),
            ({"a": "f", "b": "e", "c": "d"}),
            ({"a": "some longer string", "b": "with more data", "c": "exe"}),
        ],
    )
    def test_upt_add_new_line_ok(self, arg):
        a = upt(["a", "b", "c"])
        before = len(a.text_lines)
        a.add_new_line(arg)
        after = len(a.text_lines)
        assert after > before

    @pytest.mark.parametrize(
        "arg",
        [
            ("1:1:1"),
            ("1:2:3"),
            ("a:b:c"),
            ("f:e:d"),
            ("some longer string:with more data:exe"),
        ],
    )
    def test_upt_add_line_from_text_ok(self, arg):
        a = upt(["a", "b", "c"])
        before = len(a.text_lines)
        a.add_line_from_text(arg)
        after = len(a.text_lines)
        assert after >  before

    def test_dump_text_ok(self):
        a = upt(["a", "b", "c"])
        a.add_line_from_text("a:b:C")
        a.add_new_line({"a": 1, "b": 2, "c": 3})
        assert a.dump_text() == "a:b:C\n1:2:3\n"

    def test_load_then_dump_text_ok(self):
        a = upt(["a", "b", "c"])
        a.load_text("a:b:C\n1:2:3\n")
        a.add_line_from_text("a:b:C")
        a.add_new_line({"a": 1, "b": 2, "c": 3})
        assert a.dump_text() == "a:b:C\n1:2:3\na:b:C\n1:2:3\n"


if __name__ == "__main__":
    unittest.main()
