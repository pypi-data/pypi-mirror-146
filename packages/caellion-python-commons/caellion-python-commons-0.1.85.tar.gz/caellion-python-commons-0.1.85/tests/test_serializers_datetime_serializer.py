# test framework
import unittest
import pytest
import datetime

# package
from caellion.pycommons.serializers.datetime_serializer import DateTimeUnixSerializer
from caellion.pycommons.serializers.datetime_serializer import DateTimeUnixMillisSerializer
from caellion.pycommons.serializers.datetime_serializer import DateTimeUnixMicrosSerializer
from caellion.pycommons.serializers.datetime_serializer import DateTimeIsoTimeSerializer


# test cases
class TestSerializersDateTimeSerializer():
    @pytest.mark.parametrize(
        "input, expected",[
        ("2022-01-01T00:00:00+00:00", "2022-01-01T00:00:00+00:00"), ("2022-01-01T00:00:00-01:00", "2022-01-01T01:00:00+00:00"),]
    )
    def test_serialize_isoformat(self, input, expected):
        input = datetime.datetime.fromisoformat(input)
        assert DateTimeIsoTimeSerializer.serialize(input) == expected

    @pytest.mark.parametrize(
        "input, expected",[
        ("2022-01-01T00:00:00.000000+00:00", 1640995200), ("2022-01-01T00:00:00.000000-01:00", 1640998800),]
    )
    def test_serialize_unixseconds(self, input, expected):
        input = datetime.datetime.fromisoformat(input)
        assert DateTimeUnixSerializer.serialize(input) == expected

    @pytest.mark.parametrize(
        "input, expected",[
        ("2022-01-01T00:00:00.000000+00:00", 1640995200000), ("2022-01-01T00:00:00.000000-01:00", 1640998800000),]
    )
    def test_serialize_unixmillis(self, input, expected):
        input = datetime.datetime.fromisoformat(input)
        assert DateTimeUnixMillisSerializer.serialize(input) == expected

    @pytest.mark.parametrize(
        "input, expected",[
        ("2022-01-01T00:00:00.000000+00:00", 1640995200000000), ("2022-01-01T00:00:00.000000-01:00", 1640998800000000),]
    )
    def test_serialize_unixmicros(self, input, expected):
        input = datetime.datetime.fromisoformat(input)
        assert DateTimeUnixMicrosSerializer.serialize(input) == expected

    @pytest.mark.parametrize(
        "input, expected",[
        ("2022-01-01T00:00:00+00:00", "2022-01-01T00:00:00+00:00"), ("2022-01-01T01:00:00+00:00", "2022-01-01T01:00:00+00:00"),]
    )
    def test_deserialize_isoformat(self, input, expected):
        assert DateTimeIsoTimeSerializer.deserialize(input) == datetime.datetime.fromisoformat(expected)

    @pytest.mark.parametrize(
        "input, expected",[
        (1640995200, "2022-01-01T00:00:00+00:00"), (1640998800, "2022-01-01T01:00:00+00:00"),]
    )
    def test_deserialize_unixseconds(self, input, expected):
        assert DateTimeUnixSerializer.deserialize(input).isoformat() == expected

    @pytest.mark.parametrize(
        "input, expected",[
        (1640995200001, "2022-01-01T00:00:00.001000+00:00"), (1640998800001, "2022-01-01T01:00:00.001000+00:00"),]
    )
    def test_deserialize_unixmillis(self, input, expected):
        assert DateTimeUnixMillisSerializer.deserialize(input).isoformat() == expected

    @pytest.mark.parametrize(
        "input, expected",[
        (1640995200000001, "2022-01-01T00:00:00.000001+00:00"), (1640998800000001, "2022-01-01T01:00:00.000001+00:00"),]
    )
    def test_deserialize_unixmicros(self, input, expected):
        assert DateTimeUnixMicrosSerializer.deserialize(input).isoformat() == expected


if __name__ == "__main__":
    unittest.main()
