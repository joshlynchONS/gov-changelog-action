FROM python:3.10.5-slim

ADD gov_changelog_action /gov_changelog_action
ADD gov_changelog_action/src/template.txt /template.txt
ADD changelog-config.yml /changelog-config.yml

COPY main.py changelog-config.yml \
    entrypoint.sh requirements.txt \
    pyproject.toml setup.py setup.cfg /

RUN python -m venv vpy
RUN . vpy/bin/activate
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r /requirements.txt
RUN pip install -e .
RUN chmod +x /entrypoint.sh /main.py
ENTRYPOINT ["/entrypoint.sh"]
