# test framework
import unittest
import pytest

# package
from caellion.pycommons.encryption.tripledes import TripleDESECBMD5Key


# test cases
class TestSerializersDateTimeSerializer():
    @pytest.mark.parametrize(
        "key,data,expected",
        [
            ("C_STRVAL", "talex3_@1234", "2cYkHeYSxop72P7ZjibhVg=="), ("C_STRVAL", "talex3_@", "2cYkHeYSxoo9Zv/jq+D5Ng=="), ("C_STRVAL", "1234", "e9j+2Y4m4VY="), ("StringChar", "talex3_@1234", "vUgc8L0ArdVK+zLD4VfKhQ=="), ("StringChar", "talex3_@", "vUgc8L0ArdWQCHcU1cgi/Q=="), ("StringChar", "1234", "Svsyw+FXyoU="), ("CharString", "talex3_@1234", "t9rKj1W8bQRmV9nNTRnqvQ=="), ("CharString", "talex3_@", "t9rKj1W8bQQsBVpqtOg5lw=="), ("CharString", "1234", "ZlfZzU0Z6r0="),
        ]
    )
    def test_tripledes_ECB_MD5Key_encrypt(self, key, data, expected):
        DES = TripleDESECBMD5Key(key)
        data_ = DES.encrypt(data)
        assert data_ == expected

    @pytest.mark.parametrize(
        "key,expected,data",
        [
            ("C_STRVAL", "talex3_@1234", "2cYkHeYSxop72P7ZjibhVg=="), ("C_STRVAL", "talex3_@", "2cYkHeYSxoo9Zv/jq+D5Ng=="), ("C_STRVAL", "1234", "e9j+2Y4m4VY="), ("StringChar", "talex3_@1234", "vUgc8L0ArdVK+zLD4VfKhQ=="), ("StringChar", "talex3_@", "vUgc8L0ArdWQCHcU1cgi/Q=="), ("StringChar", "1234", "Svsyw+FXyoU="), ("CharString", "talex3_@1234", "t9rKj1W8bQRmV9nNTRnqvQ=="), ("CharString", "talex3_@", "t9rKj1W8bQQsBVpqtOg5lw=="), ("CharString", "1234", "ZlfZzU0Z6r0="),
        ]
    )
    def test_tripledes_ECB_MD5Key_decrypt(self, key, expected, data):
        DES = TripleDESECBMD5Key(key)
        data_ = DES.decrypt(data)
        assert data_ == expected


if __name__ == "__main__":
    unittest.main()
