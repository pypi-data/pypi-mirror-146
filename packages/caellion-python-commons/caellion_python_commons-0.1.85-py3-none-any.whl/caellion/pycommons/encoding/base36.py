"""!
This module provides utlilities related to converting to/from base36 encoding.
"""


class InvalidCustomCharsetLengthException(Exception):
    """!
    This exception is raised when custom character set length .
    """

    pass


class InvalidCustomCharsetException(Exception):
    """!
    This exception is raised when more than exactly one instance of a given field is contained within field list.
    """

    pass


class InvalidInputStringException(Exception):
    """!
    This exception is raised when encountering a character not defined in custom charset in input string.
    """

    pass


class NumberNotPositiveOrZeroException(Exception):
    """!
    This exception is raised when non-positive integer is passed to encode function.
    """

    pass


class ValueTooLargeException(Exception):
    """!
    This exception is raised when encountering an integer over maximum size of 16 bytes.
    """

    pass


class Base36Coder:
    """!
    This class provides methods allowing conversion between integer, hexadecimal integer and base36 strings.
    """

    # Custom charset to use with this instance of Base36Coder
    custom_charset = None

    def __init__(self, custom_charset="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        """!
        Initialize coder.

        @param custom_charset custom character set to use with the coder

        @throws InvalidCustomCharsetLengthException
        @throws InvalidCustomCharsetException
        """
        if len(custom_charset) != 36:
            raise InvalidCustomCharsetLengthException(
                "Custom charset is not exactly 36 characters long")

        xchk = []
        idx = 0
        for x in custom_charset:
            if x not in xchk:
                xchk.append(x)
                idx += 1
            else:
                idxf = custom_charset.find(x)
                raise InvalidCustomCharsetException(
                    "Character '%s' at position %s, first appeared at position %s is repeated in custom charset" % (x, idx, idxf))

        self.custom_charset = custom_charset

    def to_standard_charset(self, unformatted):
        """!
        Converts custom charset to standard charset

        @param unformatted Base36 string in custom charset encoding

        @returns Base36 string in standardized format

        @throws InvalidInputStringException
        """
        std_charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        formatted = ""

        for symbol in unformatted:
            idx = self.custom_charset.find(symbol)

            if idx == -1:
                raise InvalidInputStringException(
                    "Unexpected '%s' in input string." % symbol)
            else:
                formatted += std_charset[idx]

        return formatted

    def to_custom_charset(self, unformatted):
        """!
        Converts standard charset to custom charset

        @param unformatted Base36 string in standard charset encoding

        @returns Base36 string in custom format

        @throws InvalidInputStringException
        """
        std_charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        formatted = ""

        for symbol in unformatted:
            idx = std_charset.find(symbol)

            if idx == -1:
                raise InvalidInputStringException(
                    "Unexpected '%s' in input string." % symbol)
            else:
                formatted += self.custom_charset[idx]

        return formatted

    def bytes_to_b36(self, bytes_in):
        """!
        Converts bytes to base36 string in custom charset encoding

        @param bytes_in a bytes object to encode

        @returns Base36 string in custom format
        """
        integer = int.from_bytes(bytes_in, 'big')
        # convert to base 36
        if integer < len(self.custom_charset):
            return self.custom_charset[integer]
        b36string = ""
        while integer != 0:
            integer, i = divmod(integer, len(self.custom_charset))
            # no need to re-encode this to custom charset as it is already encoded in custom charset
            b36string = self.custom_charset[i] + b36string
        return b36string

    def int_to_b36(self, integer):
        """!
        Converts int to base36 string in custom charset encoding

        @param integer an int to encode

        @returns Base36 string in custom format

        @throws NumberNotPositiveOrZeroException
        """
        if integer < 0:
            raise NumberNotPositiveOrZeroException(
                "'%s' is not a positive or integer or zero." % integer)
        else:
            # convert to base 36
            if integer < len(self.custom_charset):
                return self.custom_charset[integer]
            b36string = ""
            while integer != 0:
                integer, i = divmod(integer, len(self.custom_charset))
                # no need to re-encode this to custom charset as it is already encoded in custom charset
                b36string = self.custom_charset[i] + b36string
            return b36string

    def b36_to_bytes(self, b36):
        """!
        Converts base36 string in custom encoding charset to bytes.

        @param b36 string in custom encoding charset

        @returns decoded bytes

        @throws InvalidInputStringException
        @throws ValueTooLargeException
        """
        integer = self.b36_to_int(b36)
        length = 1
        bytesdata = b""
        while length < 16 and bytesdata == b"":
            try:
                bytesdata = integer.to_bytes(length, byteorder='big')
                break
            except OverflowError:
                length += 1
        if length > 1 and bytesdata == b"":
            raise ValueTooLargeException(
                "Value '%s' (%s) is too large to convert to bytes (maximum 16 bytes long integer)" % (b36, integer))
        return bytesdata

    def b36_to_int(self, b36):
        """!
        Converts base36 string in custom encoding charset to integer.

        @param b36 base36 string in custom encoding charset

        @returns decoded integer

        @throws InvalidInputStringException
        """
        # decode from custom charset
        b36std = self.to_standard_charset(b36)
        # then use normal to_base
        integer = int(b36std, 36)
        return integer
