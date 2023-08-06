# test framework
import unittest
import pytest

# package
from caellion.pycommons.encoding.base36 import Base36Coder
from caellion.pycommons.encoding.base36 import ValueTooLargeException
from caellion.pycommons.encoding.base36 import NumberNotPositiveOrZeroException
from caellion.pycommons.encoding.base36 import InvalidInputStringException
from caellion.pycommons.encoding.base36 import InvalidCustomCharsetException
from caellion.pycommons.encoding.base36 import InvalidCustomCharsetLengthException


# test cases
class TestEncodingBase36Coder():
    # @pytest.mark.parametrize(
    #      "",[
    #     ("", "")],
    # )

    def test_encoding_base36_init_too_short(self):
        with pytest.raises(InvalidCustomCharsetLengthException):
            b36c = Base36Coder("0123456789ABCDEFGHIJKLMNOPQRSTUVWXY")  # noqa

    def test_encoding_base36_init_too_long(self):
        with pytest.raises(InvalidCustomCharsetLengthException):
            b36c = Base36Coder("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZZ")  # noqa

    def test_encoding_base36_init_length_ok_double_char(self):
        with pytest.raises(InvalidCustomCharsetException):
            b36c = Base36Coder("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYY")  # noqa

    def test_encoding_base36_init_ok(self):
        b36c = Base36Coder("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # noqa
        assert b36c is not None

    def test_encoding_base36_to_std_charset_invalid_input(self):
        with pytest.raises(InvalidInputStringException):
            b36c = Base36Coder("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")  # noqa
            bresult = b36c.to_standard_charset("aa")  # noqa

    @pytest.mark.parametrize(
        "input,output",
        [("ABCD", "0123"),
         ("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
          "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
         ("AAAA", "0000"),
         ("LINE", "B8D4"), ]
    )
    def test_encoding_base36_to_std_charset_valid_input(self, input, output):
        b36c = Base36Coder("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")  # noqa
        bresult = b36c.to_standard_charset(input)
        assert bresult == output

    def test_encoding_base36_to_custom_charset_invalid_input(self):
        with pytest.raises(InvalidInputStringException):
            b36c = Base36Coder("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")  # noqa
            bresult = b36c.to_custom_charset("aa")  # noqa

    @pytest.mark.parametrize(
        "input,output",
        [
            ("0123", "ABCD"),
            ("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"),
            ("0000", "AAAA"),
            ("B8D4", "LINE"), ]
    )
    def test_encoding_base36_to_custom_charset_valid_input(self, input, output):
        b36c = Base36Coder("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")  # noqa
        bresult = b36c.to_custom_charset(input)
        assert bresult == output

    def test_encoding_base36_int_to_base36_negative(self):
        with pytest.raises(NumberNotPositiveOrZeroException):
            b36c = Base36Coder("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")  # noqa
            bresult = b36c.int_to_b36(-1)

    @pytest.mark.parametrize(
        "input,output",
        [
            (b"\x00", "0"),
            (b"\x00\x00\x00\x00", "0"),
            (b"\x00\x00\x00\x01", "1"),
            (b"\x00\x00\x00\x0a", "A"),
            (b"\x00\x00\x00\x0f", "F"),
            (b"\x00\x00\x00\x10", "G"),
            (b"\x00\x00\x00\x23", "Z"),
            (b"\x00\x00\x00\x24", "10"),
            (b"\x00\x00\x00\xff", "73"),
            (b"\x00\x00\xff\xff", "1EKF"),
            (b"\x00\xff\xff\xff", "9ZLDR"),
            (b"\xff\xff\xff\xff", "1Z141Z3"),
            (b"\x01\x00\x00\x00\x00", "1Z141Z4"),
            (b"\x00\x00\x00\x01\x00\x00\x00\x00", "1Z141Z4"),
            (b"\xff\xff\xff\xff\xff\xff\xff\xff", "3W5E11264SGSF"),
        ]
        # 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ
    )
    def test_encoding_base36_bytes_to_b36_default_charset_valid_input(self, input, output):
        b36c = Base36Coder()  # noqa
        bresult = b36c.bytes_to_b36(input)
        assert bresult == output

    @pytest.mark.parametrize(
        "input,output",
        [
            (0, "0"),
            (1, "1"),
            (10, "A"),
            (15, "F"),
            (16, "G"),
            (35, "Z"),
            (36, "10"),
            (255, "73"),
            (65535, "1EKF"),
            (16777215, "9ZLDR"),
            (4294967295, "1Z141Z3"),
            (4294967296, "1Z141Z4"),
            (18446744073709551615, "3W5E11264SGSF"),
        ]
        # 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ
    )
    def test_encoding_base36_int_to_b36_default_charset_valid_input(self, input, output):
        b36c = Base36Coder()  # noqa
        bresult = b36c.int_to_b36(input)
        assert bresult == output

    def test_encoding_base36_to_int_negative(self):
        with pytest.raises(InvalidInputStringException):
            b36c = Base36Coder()  # noqa
            bresult = b36c.b36_to_int("-A")

    @pytest.mark.parametrize(
        "input,output",
        [
            ("0", 0),
            ("1", 1),
            ("A", 10),
            ("F", 15),
            ("G", 16),
            ("Z", 35),
            ("10", 36),
            ("73", 255),
            ("1EKF", 65535),
            ("9ZLDR", 16777215),
            ("1Z141Z3", 4294967295),
            ("1Z141Z4", 4294967296),
            ("3W5E11264SGSF", 18446744073709551615),
        ]
        # 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ
    )
    def test_encoding_base36_to_int_valid_input(self, input, output):
        b36c = Base36Coder()  # noqa
        bresult = b36c.b36_to_int(input)
        assert bresult == output

    def test_encoding_base36_to_bytes_negative(self):
        with pytest.raises(InvalidInputStringException):
            b36c = Base36Coder()  # noqa
            bresult = b36c.b36_to_int("-A")

    @pytest.mark.parametrize(
        "input,output",
        [
            ("0", b"\x00"),
            ("1", b"\x01"),
            ("A", b"\x0a"),
            ("F", b"\x0f"),
            ("G", b"\x10"),
            ("Z", b"\x23"),
            ("10", b"\x24"),
            ("73", b"\xff"),
            ("1EKF", b"\xff\xff"),
            ("9ZLDR", b"\xff\xff\xff"),
            ("1Z141Z3", b"\xff\xff\xff\xff"),
            ("1Z141Z4", b"\x01\x00\x00\x00\x00"),
            ("3W5E11264SGSF", b"\xff\xff\xff\xff\xff\xff\xff\xff"),
        ]
        # 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ
    )
    def test_encoding_base36_to_bytes_valid_input(self, input, output):
        b36c = Base36Coder()  # noqa
        bresult = b36c.b36_to_bytes(input)
        assert bresult == output

    def test_encoding_base36_to_bytes_too_large(self):
        with pytest.raises(ValueTooLargeException):
            b36c = Base36Coder()  # noqa
            bresult = b36c.b36_to_bytes('2ZZZZZZZZZZZZZZZZZZZZZZZ')


if __name__ == "__main__":
    unittest.main()
