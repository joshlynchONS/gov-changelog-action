#!/bin/sh -l

set -e

python -m pip install --upgrade pip setuptools wheel
pip install -r /requirements.txt

python /main.py /src/get_github_data.py /src/manip_data.py /src/create_changelog.py /src/template.txt /changelog-config.yml
