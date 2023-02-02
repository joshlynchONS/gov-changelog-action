FROM python:3.10.5-slim

COPY main.py changelog-config.yml gov_changelog_action/src/template.txt gov_changelog_action/src/get_github_data.py gov_changelog_action/src/manip_data.py gov_changelog_action/src/create_changelog.py entrypoint.sh requirements.txt /
RUN chmod +x /entrypoint.sh /main.py
ENTRYPOINT ["/entrypoint.sh"]
