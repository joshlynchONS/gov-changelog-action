FROM python:3.10.5-slim

ADD gov_changelog_action /gov_changelog_action
ADD template.txt /template.txt

COPY main.py changelog-config.yml \
    gov_changelog_action/src/get_github_data.py gov_changelog_action/src/manip_data.py \
    gov_changelog_action/src/create_changelog.py entrypoint.sh requirements.txt \
    pyproject.toml setup.py setup.cfg /

RUN python -m venv vpy
RUN . vpy/bin/activate
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r /requirements.txt
RUN ls
RUN pip install -e .
RUN chmod +x /entrypoint.sh /main.py
ENTRYPOINT ["/entrypoint.sh"]
