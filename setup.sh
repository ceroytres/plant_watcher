#!/usr/bin/env bash

set -e

#check python
if [[ "$(python -c "import sys; print(''.join(sys.version[0:3:2]))")" -lt "37" ]]; then
    printf "Aliasing python3 as python"
    alias python=python3.7
fi


python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

