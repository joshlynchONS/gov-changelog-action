FROM 3.10.9-windowsservercore-1809

COPY main.py changelog-config.yml gov_changelog_action/src/template.txt \
    gov_changelog_action/src/get_github_data.py gov_changelog_action/src/manip_data.py \
    gov_changelog_action/src/create_changelog.py entrypoint.sh requirements.txt \
    pyproject.toml setup.py setup.cfg /

RUN chmod +x /entrypoint.sh /main.py
ENTRYPOINT ["/entrypoint.sh"]
