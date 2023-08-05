"""
Pyntegrity is Python package that helps checking a file integrity.
Copyright (C) 2022  Salah OSFOR

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import re
import hashlib
from pathlib import Path

from .exceptions import FileNotFoundException
from .exceptions import ObjectNotAFileException
from .exceptions import HashStrNotValidException
from .exceptions import MissingFilePermissionException
from .exceptions import HashAlgorithmNotSupportedException
from .exceptions import DetectedHashAlgorithmNotSupportedException

from .config import VERSION
from .config import SUPPORTED_HASH_ALGOS


def get_version():
    return VERSION


def detect_hash_algo(checksum_str: str):
    """
    Detects hash algorithm based on its length.

    :param checksum_str: the hash string
    :return: the name of the hash algorithm
    :raises DetectedHashAlgorithmNotSupportedException: raised if the hash
        length isn't valid for any supported algorithm
    """
    hash_len = len(checksum_str)
    for name, infos in SUPPORTED_HASH_ALGOS.items():
        if infos["LENGTH"] == hash_len:
            if validate_checksum_str(checksum_str=checksum_str, hash_algo=name):
                return name
    else:
        raise DetectedHashAlgorithmNotSupportedException(
            detected_length=hash_len, checksum_str=checksum_str
        )


def validate_checksum_str(checksum_str: str, hash_algo: str):
    """
    Checks if the str is a valid checksum in the detected algorithm

    :param checksum_str:the hash string
    :param hash_algo: the hash algorithm
    :return: True if valid
    :raises HashStrNotValidException: raised if the hash str isn't valid
    """
    hash_name = hash_algo
    pattern = re.compile(SUPPORTED_HASH_ALGOS[hash_name]["REX"])
    if pattern.match(checksum_str):
        return True
    else:
        raise HashStrNotValidException(
            detected_hash_algo=hash_name, checksum_str=checksum_str
        )


def get_file_path_from_str(str_path: str):
    """
    Checks if path is a file and there is read access to it then return a Path object

    :param str_path: provided file path
    :return: file path
    :rtype: Path
    """
    path_object = Path(str_path)
    if path_object.is_file():
        path_object = path_object.resolve()
        if os.access(path_object, os.R_OK):
            return path_object
        else:
            raise MissingFilePermissionException(file_path=str_path)
    elif not path_object.exists():
        raise FileNotFoundException(file_path=str_path)
    else:
        raise ObjectNotAFileException(file_path=str_path)


def calculate_file_checksum(file_path: str, checksum_algo: str):
    """
    Calculate file checksum

    :param file_path: target file path
    :param checksum_algo: the name of hash algo that will be used for the checksum
    :return: return file checksum
    """
    if checksum_algo.lower() in SUPPORTED_HASH_ALGOS:
        file = get_file_path_from_str(file_path)
        hashlib_obj = hashlib.new(checksum_algo)
        with file.open() as file_to_validate:
            file_content = file_to_validate.read()
            hashlib_obj.update(file_content.encode())
            return hashlib_obj.hexdigest()
    else:
        raise HashAlgorithmNotSupportedException(checksum_algo)


class IntegrityValidator:
    def __init__(self, str_path: str, checksum_str: str):
        """
        A class to validate file integrity using a checksum string

        :param str_path: the path of the target file
        :param checksum_str:
        """
        self.hash_algo = detect_hash_algo(checksum_str=checksum_str)
        self.checksum_str = checksum_str
        self.file_path = str_path

    def validate_file_integrity(self):
        """
        Function to validate the file integrity
        :return: True is the file valid, False if not
        """
        file_checksum = self.get_file_checksum(self.hash_algo)
        return file_checksum == self.checksum_str

    def get_file_checksum(self, hash_algo: str):
        """
        Calculate file checksum

        :param hash_algo: the name of hash algo that will be used for the checksum
        :return: return file checksum
        """
        return calculate_file_checksum(self.file_path, hash_algo)
