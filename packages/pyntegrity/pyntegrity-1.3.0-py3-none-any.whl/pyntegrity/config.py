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
# Hash settings

SHA512_LENGTH = 128
SHA256_LENGTH = 64
MD5_LENGTH = 32

SHA512_REX = r"^[A-Fa-f\d]{128}$"
SHA256_REX = r"^[A-Fa-f\d]{64}$"
MD5_REX = r"^[a-fA-F\d]{32}$"

SUPPORTED_HASH_ALGOS = {
    "sha256": {"REX": SHA256_REX, "LENGTH": SHA256_LENGTH},
    "md5": {"REX": MD5_REX, "LENGTH": MD5_LENGTH},
    "sha512": {"REX": SHA512_REX, "LENGTH": SHA512_LENGTH},
}

VERSION = "1.3.0"
