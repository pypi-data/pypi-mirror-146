# test framework
import unittest
import pytest
import binascii

# package
from caellion.pycommons.hashing.file_hashing import FileHasher, NotDoneYetException, AlreadyDoneException, UnsupportedAlgorithmException  # noqa: F401

TEST_DATA_PATH = "tests/testdata/hashing/file_hashing/"

TEST_PARAMETERIZED_LIST = [
    # Empty file in 01.bin
    ("01.bin", "", "da39a3ee5e6b4b0d3255bfef95601890afd80709"),
    ("01.bin", None, "da39a3ee5e6b4b0d3255bfef95601890afd80709"),
    ("01.bin", "sha1", "da39a3ee5e6b4b0d3255bfef95601890afd80709"),
    ("01.bin", "sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("01.bin", "sha384", "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b"),
    ("01.bin", "sha512", "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"),
    ("01.bin", "md5", "d41d8cd98f00b204e9800998ecf8427e"),
    # UTF16-LE Strings in 02.bin
    ("02.bin", "sha1", "752f931aa0c4b7a942ceff6f35ecf73bf84723f7"),
    ("02.bin", "sha256", "2379d57ca5836d99c3b19fa06611fdbf3240d25597bb813768cacc10064a1773"),
    ("02.bin", "sha384", "f8bd72222ecc74c456fb96ba1dd049a37a2b643af64a5e811a08a9a2c507b1efecb0033ab7fb9560e1e3a17d3f6dc607"),
    ("02.bin", "sha512", "d40223f1c63c75b457be72ed6959b2a3bda8ba36f12f2bd6db882b04892cfac37874aa496a23f1d63e77a7afef6fb04c52533fe0fc67a6e178357e4f38324450"),
    ("02.bin", "md5", "9756321f9c028d259e79fb074e17149e"),
    # Random binary in 03.bin
    ("03.bin", "sha1", "a3a14d1f4115e8280e87e1eeb91fa89dcccb1a37"),
    ("03.bin", "sha256", "1c527e0612df82e21032f39774507541813db0809fa5809ed1707231684219e4"),
    ("03.bin", "sha384", "a9f9364ea82117a6edf0769d51e8da4dce89b0114b75d143583a1309094b4d9b40a279927b152335c84adfa391550760"),
    ("03.bin", "sha512", "e9652220c97b6b8c511be78c4924f89e84f86f0d78fbfa8a9a46f5c559b26140f45f70c44cc61e5b570cc3ad64a327e25f0de13180352caa4eb4d1f53cd556cb"),
    ("03.bin", "md5", "db4a90ecad9e87970d6fc6e30ccbf8ee"),
    # Random binary in 04.bin (10MB file)
    ("04.bin", "sha1", "66edb5278033be74dbfeb06693701fce60b8236c"),
    ("04.bin", "sha256", "5f44e1370f6cb59f0fa47df86ede5a55226580f6471b44159fe8372a105392da"),
    ("04.bin", "sha384", "9fa04d1f69d44492c3a4c8fb48be4146dbc1c3b739e3f45e2abaf64051a55f592ce4ec87bdfc74db53ef5bdfbe1e071f"),
    ("04.bin", "sha512", "73f18b99cc8bbd5da23e961d5edfd4ceeab3f7a328785f9c0a46f66aaaf89e541690cebef3a450f23dcc327122c08a791221454500e87ee6e4b9d39dbb39413c"),
    ("04.bin", "md5", "bba058fa7e56035c7435da960140155d"),
]


# test cases
class TestHashingFileHasher():

    maxDiff = None

    # exceptions
    def test_unsupported_algorithm(self):
        with pytest.raises(UnsupportedAlgorithmException):
            FH = FileHasher("md4")  # noqa

    def test_get_hexdigest_not_done_hash_bytes(self):
        with pytest.raises(NotDoneYetException):
            FH = FileHasher("md5")  # noqa
            FH.get_hashbytes()

    def test_get_hexdigest_not_done_hash_hex(self):
        with pytest.raises(NotDoneYetException):
            FH = FileHasher("md5")  # noqa
            FH.get_hexdigest()

    def test_cannot_hash_twice_raw(self):
        with pytest.raises(AlreadyDoneException):
            FH = FileHasher("md5")  # noqa
            with open(TEST_DATA_PATH + "01.bin", "rb") as f:
                FH.hash_file(f)
                FH.hash_file(f)

    def test_cannot_hash_twice_path(self):
        with pytest.raises(AlreadyDoneException):
            FH = FileHasher("md5")  # noqa
            FH.hash_path(TEST_DATA_PATH + "01.bin")
            FH.hash_path(TEST_DATA_PATH + "01.bin")

    @pytest.mark.parametrize("path,algo,expected",TEST_PARAMETERIZED_LIST)
    def test_hashes_file_ok_raw(self, path, algo, expected):
        FH = FileHasher(algo)  # noqa
        with open(TEST_DATA_PATH + path, "rb") as f:
            FH.hash_file(f)
        result = FH.get_hashbytes()
        assert result == binascii.unhexlify(expected)

    @pytest.mark.parametrize("path,algo,expected",TEST_PARAMETERIZED_LIST)
    def test_hashes_file_ok_hexdigest(self, path, algo, expected):
        FH = FileHasher(algo)  # noqa
        with open(TEST_DATA_PATH + path, "rb") as f:
            FH.hash_file(f)
        result = FH.get_hexdigest()
        assert result == expected

    @pytest.mark.parametrize("path,algo,expected",TEST_PARAMETERIZED_LIST)
    def test_hashes_path_ok_raw(self, path, algo, expected):
        FH = FileHasher(algo)  # noqa
        FH.hash_path(TEST_DATA_PATH + path)
        result = FH.get_hashbytes()
        assert result == binascii.unhexlify(expected)

    @pytest.mark.parametrize("path,algo,expected",TEST_PARAMETERIZED_LIST)
    def test_hashes_path_ok_hexdigest(self, path, algo, expected):
        FH = FileHasher(algo)  # noqa
        FH.hash_path(TEST_DATA_PATH + path)
        result = FH.get_hexdigest()
        assert result == expected

    @pytest.mark.parametrize("path,algo,expected",TEST_PARAMETERIZED_LIST)
    def test_hashes_file_ok_raw_combo(self, path, algo, expected):
        FH = FileHasher(algo)  # noqa
        with open(TEST_DATA_PATH + path, "rb") as f:
            result = FH.hash_file_and_get_hashbytes(f)
        assert result == binascii.unhexlify(expected)

    @pytest.mark.parametrize("path,algo,expected",TEST_PARAMETERIZED_LIST)
    def test_hashes_file_ok_hexdigest_combo(self, path, algo, expected):
        FH = FileHasher(algo)  # noqa
        with open(TEST_DATA_PATH + path, "rb") as f:
            result = FH.hash_file_and_get_hexdigest(f)
        assert result == expected

    @pytest.mark.parametrize("path,algo,expected",TEST_PARAMETERIZED_LIST)
    def test_hashes_path_ok_raw_combo(self, path, algo, expected):
        FH = FileHasher(algo)  # noqa
        result = FH.hash_path_and_get_hashbytes(TEST_DATA_PATH + path)
        assert result == binascii.unhexlify(expected)

    @pytest.mark.parametrize("path,algo,expected",TEST_PARAMETERIZED_LIST)
    def test_hashes_path_ok_hexdigest_combo(self, path, algo, expected):
        FH = FileHasher(algo)  # noqa
        result = FH.hash_path_and_get_hexdigest(TEST_DATA_PATH + path)
        assert result == expected


if __name__ == "__main__":
    unittest.main()
