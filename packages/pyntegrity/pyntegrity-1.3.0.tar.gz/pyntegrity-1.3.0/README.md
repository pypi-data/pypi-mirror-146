# Pyntegrity

Pyntegrity is Python package that helps you check a file integrity. 

![master workflow](https://github.com/ddalu5/pyntegrity/actions/workflows/ci.yml/badge.svg?branch=main)

## Supported Python versions

Tested on:

- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10

## Documentation

Latest version is 1.2.0

## Installation

To install Pyntegrity use pip:

`pip install pyntegrity`

### Supported features

#### Checksum algorithms

The supported checksum algorithms are:

- md5
- sha256
- sha512

#### Target files sizes

For now mostly small files since it loads the whole file in memory to calculate its checksum

#### How to use

In your program import the class `IntegrityValidator`:

```python
from pyntegrity.core import IntegrityValidator
```

Initialize it with the target file and the expected checksum 
(it automatically detects which checksum algorithm to use), example:

```python
obj = IntegrityValidator(
            str_path="my_file.txt",
            checksum_str="my_checksum",
        )
```

Then use the function `validate_file_integrity` to check the file integrity, 
it returns `True` if the target file checksum equal the one passed in the class constructor,
if else it returns `False`, example:

```python

status = obj.validate_file_integrity()
```

#### Side note

Right now it will open anyfile in text mode (even binary).

### Future features

- Support more file type modes
- Support more checksum algorithms
- Support for big files

## License

GPL-3.0 see [license content](https://github.com/ddalu5/pyntegrity/blob/main/LICENSE)