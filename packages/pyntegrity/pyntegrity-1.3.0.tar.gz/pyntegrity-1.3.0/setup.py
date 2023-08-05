from pyntegrity import get_version
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyntegrity",
    version=get_version(),
    description="Pyntegrity is a Python package that helps you check a file integrity.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddalu5/pyntegrity",
    author="Salah OSFOR",
    author_email="osfor.salah@gmail.com",
    license="GPL-3.0",
    packages=find_packages(include=["pyntegrity"]),
    test_suite="tests",
    tests_require=["unittest", "black", "pytest", "coverage"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)
