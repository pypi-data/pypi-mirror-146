"""!
This module provides utlilities related to creating, reading, writing and parsing of linux-style passwd/shadow file.
"""


class DuplicateFieldException(Exception):
    """!
    This exception is raised when more than exactly one instance of a given field is contained within field list.
    """

    pass


class EmptyFieldNameException(Exception):
    """!
    This exception is raised when an empty field name is encountered.
    """

    pass


class SeparatorEmptyException(Exception):
    """!
    This exception is raised when an empty separator string is encountered.
    """

    pass


class NewlineEmptyException(Exception):
    """!
    This exception is raised when an empty line separator string is encountered.
    """

    pass


class InvalidFileFormatException(Exception):
    """!
    This exception is raised when encountering invalid or non-uniform line.
    """

    pass


class UnixPasswordText:
    """!
    This class provides methods to read and write to linux-style passwd/shadow files, ability to parse shadow-style lines into dicts and identifying password hashing algorithms used in linux-style hash format.
    """

    text_lines = []  # list of dicts representing lines
    line_format = []  # list of field names to use as line format
    separator = ":"  # string separating fields in line
    newline = "\n"  # string to use as line separator when dumping text

    def __init__(self, line_format, separator=":", newline="\n"):
        """!
        Initialize parser.

        @param line_format List of field names, field names have to be unique and cannot be empty. Not all fields have to be in format list if dumping text.
        @param separator String to use to separate fields in line
        @param newline String to use as line separator
        """
        # validate field list
        check_ = []
        for x in line_format:
            if x not in check_:
                check_.append(x)
            else:
                raise DuplicateFieldException("Field '%s' is duplicated in field list." % x)
            if x == "" or x is None:
                raise EmptyFieldNameException("Encountered empty field name in field list.")

        if separator is None or separator == "":
            raise SeparatorEmptyException("Encountered empty separator string.")

        if newline is None or newline == "":
            raise NewlineEmptyException("Encountered empty line separator string.")

        self.line_format = line_format
        self.separator = separator
        self.newline = newline
        self.text_lines = []  # need to cleanup this on init (tests somehow keep state unpredictably)

    def parse_line(self, line):
        """!
        Parses line according to line_format.

        @param line The line to be parsed

        @returns The dict representation of given line
        """
        split_line = line.split(self.separator)

        fieldid = 0
        linedict = {}
        for x in split_line:
            # find name in field list
            if fieldid > (len(self.line_format) - 1):
                raise InvalidFileFormatException("Field with value '%s' is outside defined line format," % x)
            fname = self.line_format[fieldid]
            fvalue = x
            linedict.update({fname: fvalue})
            fieldid += 1

        return linedict

    def create_line(self, fields):
        """!
        Creates string line from fieldset and line_format

        @param fields Dict of field values to fill line with

        @returns String representation of give line data
        """
        line = ""
        fieldno = 0
        for x in self.line_format:
            linedata = fields[x]

            line += str(linedata)
            if fieldno < (len(self.line_format) - 1):
                line += str(self.separator)

            fieldno += 1

        return line

    def add_new_line(self, fields):
        """!
        Prepares and adds new line to internal buffer.

        @param fields Dict of field values to add to internal buffer as a line
        """
        self.text_lines.append(fields)

    def add_line_from_text(self, line):
        """!
        Parsed line and adds appropriate dict to internal buffer.

        @param line String representation of a given line
        """
        self.text_lines.append(self.parse_line(line))

    def dump_text(self):
        """!
        Prepares and returns text block representing all lines in internal buffer.

        @returns String block representing internal buffer. Empty string when no lines in buffer.
        """
        linestr = ""
        for x in self.text_lines:
            linestr += self.create_line(x) + self.newline

        return linestr

    def load_text(self, textblock):
        """!
        Parses text block and adds its lines to internal buffer.

        @param textblock String to load into internal buffer
        """
        lines = textblock.split(self.newline)

        for line in lines:
            line = line.strip()
            if line is not None and line != "":
                self.add_line_from_text(line)
