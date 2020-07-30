#!/usr/bin/env bash

#check python
if [[ "$(python -c "import sys; print(sys.version[0])")" -ne "3" ]]; then
    printf "Aliasing python3 as python"
    alias python=python3
fi


python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

