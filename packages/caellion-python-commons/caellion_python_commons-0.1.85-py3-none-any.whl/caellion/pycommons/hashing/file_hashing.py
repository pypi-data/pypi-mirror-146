"""!
This module provides utilities related to hashing files
"""

import hashlib


class UnsupportedAlgorithmException(Exception):
    """!
    This exception is raised whenever provided algorithm is not one of allowed algorithms.
    """

    pass


class AlreadyDoneException(Exception):
    """!
    This exception is raised when hashing was requested on a FileHasher that has already finished hashing.
    """

    pass


class NotDoneYetException(Exception):
    """!
    This exception is raised when a hash was requested from a FileHasher that has not hashed any file yet.
    """

    pass


class FileHasher:
    """!
    This class provides hashlib-based file hasher
    """

    ## Instance of hashlib algorithm implementation
    hashlib_instance = None
    ## Is this FileHasher done hashing a file
    islocked = False
    ## result of hashing (raw)
    digest = None
    ## result of hashing  (hex)
    hexdigest = None

    def __init__(self, algo=None):
        """!
        Initializes hasher

        Currently supported hashes: SHA1, SHA256, SHA384, SHA512, MD5 (not recommended)

        @param algo String with name of algorithm to use

        @throws UnsupportedAlgorithmException when attempting to use unsupported algorithm
        """
        if algo is None or algo.lower() == "" or algo.lower() == "sha1":
            self.hashlib_instance = hashlib.sha1()
        elif algo.lower() == "sha256":
            self.hashlib_instance = hashlib.sha256()
        elif algo.lower() == "sha384":
            self.hashlib_instance = hashlib.sha384()
        elif algo.lower() == "sha512":
            self.hashlib_instance = hashlib.sha512()
        elif algo.lower() == "md5":
            self.hashlib_instance = hashlib.md5()
        else:
            raise UnsupportedAlgorithmException("'%s' is not allowed as a hashing algorithm." % (algo,))

    def hash_file(self, file):
        """!
        Hashes file-object with currently chosen algorithm

        @param file file-object to be hashed

        @throws AlreadyDoneException if this FileHasher is already done hashing a different file
        """
        if self.islocked:
            raise AlreadyDoneException()
        b = bytearray(128 * 1024)
        mv = memoryview(b)
        for n in iter(lambda: file.readinto(mv), 0):
            self.hashlib_instance.update(mv[:n])
        self.digest = self.hashlib_instance.digest()
        self.hexdigest = self.hashlib_instance.hexdigest()
        self.islocked = True

    def hash_path(self, path):
        """!
        Hashes file-object with currently chosen algorithm

        @param path path to file to be hashed

        @throws AlreadyDoneException if this FileHasher is already done hashing a different file
        """
        if self.islocked:
            raise AlreadyDoneException()
        b = bytearray(128 * 1024)
        mv = memoryview(b)
        with open(path, "rb", buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                self.hashlib_instance.update(mv[:n])
        self.digest = self.hashlib_instance.digest()
        self.hexdigest = self.hashlib_instance.hexdigest()
        self.islocked = True

    def get_hexdigest(self):
        """!
        Returns hexadecimal value of hash from this object.

        @returns hexadecimal string representation of hash

        @throws NotDoneYetException if no file was hashed with this FileHasher.
        """
        if self.islocked:
            return self.hexdigest
        else:
            raise NotDoneYetException()

    def get_hashbytes(self):
        """!
        Returns hexadecimal value of hash from this object.

        @returns bytes of hash

        @throws NotDoneYetException if no file was hashed with this FileHasher.
        """
        if self.islocked:
            return self.digest
        else:
            raise NotDoneYetException()

    def hash_file_and_get_hashbytes(self, file):
        """!
        Hashes a file-object and returns hash

        @param file file-object to be hashed

        @returns bytes of hash

        @throws AlreadyDoneException if this FileHasher is already done hashing a different file
        """
        self.hash_file(file)
        return self.get_hashbytes()

    def hash_path_and_get_hashbytes(self, path):
        """!
        Hashes a file at path and returns hash

        @param path path to the file to be hashed

        @returns bytes of hash

        @throws AlreadyDoneException if this FileHasher is already done hashing a different file
        """
        self.hash_path(path)
        return self.get_hashbytes()

    def hash_file_and_get_hexdigest(self, file):
        """!
        Hashes a file-object and returns hash

        @param file file-object to be hashed

        @returns hexadecimal string representation of hash

        @throws AlreadyDoneException if this FileHasher is already done hashing a different file
        """
        self.hash_file(file)
        return self.get_hexdigest()

    def hash_path_and_get_hexdigest(self, path):
        """!
        Hashes a file at path and returns hash

        @param path path to the file to be hashed

        @returns hexadecimal string representation of hash

        @throws AlreadyDoneException if this FileHasher is already done hashing a different file
        """
        self.hash_path(path)
        return self.get_hexdigest()
