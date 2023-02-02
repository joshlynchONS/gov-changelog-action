#!/bin/sh -l

set -e

python -m pip install --upgrade pip setuptools wheel
pip install -r /requirements.txt
python -r /setup.py install

python /main.py /gov_changelog_action/src/get_github_data.py /gov_changelog_action/src/manip_data.py /gov_changelog_action/src/create_changelog.py /gov_changelog_action/src/template.txt /changelog-config.yml
