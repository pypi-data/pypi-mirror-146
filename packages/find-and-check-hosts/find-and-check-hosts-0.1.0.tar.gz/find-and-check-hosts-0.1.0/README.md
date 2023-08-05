# find-and-check-hosts 

Searches files for IPs and hostnames and checks them against a rule list to prevent accidentially leaking sensitive information.

## Installation

This repo can now be installed with pip:
```
pip install find-and-check-hosts
```

Or you can install it manually by following these steps:

1. Clone this repository
2. Install the dependencies listed in `./requirements.txt` with pip
3. (Optional) Do a `pip install .` to add the `find-and-check-hosts` command to your PATH

## Usage

If you did the pip installation, you should be able to just call the installed script:
```
find-and-check-hosts <arguments>
```

If you just cloned it, you need to call it by path:
```
./src/main.py <arguments>
```

