#!/usr/bin/env bash

set -e
set -x

python3 -m venv .venv

source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt --no-cache-dir

