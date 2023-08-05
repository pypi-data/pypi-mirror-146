import argparse

from pyntegrity.core import get_version
from pyntegrity.core import IntegrityValidator
from pyntegrity.core import calculate_file_checksum

from pyntegrity.config import SUPPORTED_HASH_ALGOS

parser = argparse.ArgumentParser(
    description="Pyntegrity is a Python package that helps you check a file integrity."
)
parser.add_argument(
    "-v",
    "--version",
    action="store_true",
    help="Print Pyntegrity current version",
)
parser.add_argument(
    "-f", "--file", metavar="FILE_PATH", type=str, help="Target file path"
)
parser.add_argument(
    "-c",
    "--calculate-checksum",
    metavar="CHECKSUM_ALGO_NAME",
    type=str,
    help="Calculate target file checksum based on the given algorithm name, expects an algorithm name!",
)
parser.add_argument(
    "-l",
    "--list-algorithms",
    action="store_true",
    help="List supported checksum algorithms",
)
parser.add_argument(
    "-i",
    "--integrity-verification",
    metavar="CHECKSUM_STR",
    type=str,
    help="Verifies the integrity of a target file based on the given checksum, expects a checksum!",
)

args = parser.parse_args()


if __name__ == "__main__":
    if args.version:
        print(get_version())

    if args.list_algorithms:
        print("[+] The supported checksum algorithms are:\n")
        algos = list(SUPPORTED_HASH_ALGOS.keys())
        algos.sort()
        for algo in algos:
            print(f"\t- {algo}")

    if args.calculate_checksum is not None:
        if args.file is not None:
            print(
                calculate_file_checksum(
                    file_path=args.file, checksum_algo=args.calculate_checksum
                )
            )
        else:
            raise Exception("[!] -c [--calculate-checksums] requires -f [--file]")

    if args.integrity_verification is not None:
        if args.file is not None:
            i_validator = IntegrityValidator(
                str_path=args.file, checksum_str=args.integrity_verification
            )
            if i_validator.validate_file_integrity():
                print("[+] File integrity is valid!")
            else:
                print("[!] File integrity is not valid!")
                exit(1)
        else:
            raise Exception("[!] -i [--integrity-verification] requires -f [--file]")
