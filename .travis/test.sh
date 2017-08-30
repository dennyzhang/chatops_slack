#!/bin/bash -e
find . -name "*.py" | grep -v chatops.py | xargs pylint -E
