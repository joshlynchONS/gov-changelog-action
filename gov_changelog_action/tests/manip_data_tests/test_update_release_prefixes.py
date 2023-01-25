import pytest
import json
from gov_changelog_action.src.manip_data import update_release_prefixes

cases = json.load(
    open(
        "gov_changelog_action/tests/manip_data_tests/update_release_prefixes_testcase"
        ".json"
    )
)


class Prefix:
    def __init__(self, prefix):
        self.prefix = prefix


class Release:
    def __init__(self, tag):
        self.tag = tag
        self.prefixes = []

    def update_prefixes(self, commit_prefix):
        if commit_prefix not in self.prefixes:
            self.prefixes.append(commit_prefix)


class Commit:
    def __init__(self, release, prefix):
        self.release = release
        self.prefix = prefix


def make_commit_class(commits):
    list_commits = []
    for commit in commits:
        release = commit["release"]
        prefix = commit["prefix"]
        temp = Commit(release, prefix)
        list_commits.append(temp)
    return list_commits


def make_release_class(releases):
    list_releases = []
    for release in releases:
        tag = release["tag"]
        temp = Release(tag)
        list_releases.append(temp)
    return list_releases


def make_prefix_class(prefixes):
    list_prefix = []
    for prefix in prefixes:
        prefix = prefix["prefix"]
        temp = Prefix(prefix)
        list_prefix.append(temp)
    return list_prefix


@pytest.fixture
def test_case_1():
    releases = cases["test case 1"]["releases"]
    releases = make_release_class(releases)
    commits = cases["test case 1"]["commits"]
    commits = make_commit_class(commits)
    prefixes = cases["test case 1"]["prefixes"]
    prefixes = make_prefix_class(prefixes)

    updated_releases = update_release_prefixes(releases, commits, prefixes)
    return updated_releases


class TestUpdateReleasePrefixes1:
    def test_releases_prefixes(self, test_case_1):
        assert test_case_1[0].prefixes[0].prefix == "add"
        assert test_case_1[0].prefixes[1].prefix == "change"
        assert test_case_1[1].prefixes[0].prefix == "fix"

    def test_number_prefixes_added(self, test_case_1):
        assert len(test_case_1[0].prefixes) == 2
        assert len(test_case_1[1].prefixes) == 1

    def test_number_releases(self, test_case_1):
        assert len(test_case_1) == len(cases["test case 1"]["releases"])
