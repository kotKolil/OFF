#!/bin/bash

# Delete all files except .bat, .sh, and .py
find . -type f ! -name '*.bat' ! -name '*.sh' ! -name '*.py' -exec rm -v {} +

pytest -vv

# Delete all files except .bat, .sh, and .py
find . -type f ! -name '*.bat' ! -name '*.sh' ! -name '*.py' -exec rm -v {} +