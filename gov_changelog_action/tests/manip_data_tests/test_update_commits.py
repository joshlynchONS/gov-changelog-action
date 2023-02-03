import pytest
import json
from gov_changelog_action.src.manip_data import update_commits

cases = json.load(
    open("gov_changelog_action/tests/manip_data_tests/update_commits_testcase.json")
)


class DummyCommit:
    def __init__(self, message):
        self.message = message


class Commit:
    def __init__(self, message, sha):
        self.commit = DummyCommit(message)
        self.sha = sha


def make_commit_class(commits):
    list_commits = []
    for commit in commits:
        message = commit["message"]
        sha = commit["sha"]
        temp = Commit(message, sha)
        list_commits.append(temp)
    return list_commits


@pytest.fixture
def test_case_1():
    tags_sha_dict = cases["test case 1"]["tags_sha_dict"]
    commits = cases["test case 1"]["commits"]
    commits = make_commit_class(commits)
    unreleased_bool = cases["test case 1"]["unreleased_bool"]
    updated_commits = update_commits(tags_sha_dict, commits, unreleased_bool)
    return updated_commits


@pytest.fixture
def test_case_2():
    tags_sha_dict = cases["test case 2"]["tags_sha_dict"]
    commits = cases["test case 2"]["commits"]
    commits = make_commit_class(commits)
    unreleased_bool = cases["test case 2"]["unreleased_bool"]
    updated_commits = update_commits(tags_sha_dict, commits, unreleased_bool)
    return updated_commits


class TestUpdateCommits1:
    def test_number_commits(self, test_case_1):
        assert len(test_case_1) == len(cases["test case 1"]["commits"])

    def test_message_commits(self, test_case_1):
        assert test_case_1[0].message == cases["test case 1"]["commits"][0]["message"]
        assert test_case_1[1].message == cases["test case 1"]["commits"][1]["message"]

    def test_commit_releases(self, test_case_1):
        assert test_case_1[0].release == "Unreleased"
        assert test_case_1[1].release == "v0.0.1"


class TestUpdateCommits2:
    def test_number_commits(self, test_case_2):
        assert len(test_case_2) == (len(cases["test case 2"]["commits"]) - 1)

    def test_message_commits(self, test_case_2):
        assert test_case_2[0].message == cases["test case 2"]["commits"][1]["message"]

    def test_commit_releases(self, test_case_2):
        assert test_case_2[0].release == "v0.0.1"


class TestUpdateCommits3:
    def test_unreleased_bool_type(self):
        tags_sha_dict = cases["test case 3"]["tags_sha_dict"]
        commits = cases["test case 3"]["commits"]
        commits = make_commit_class(commits)
        unreleased_bool = cases["test case 3"]["unreleased_bool"]
        with pytest.raises(ValueError):
            self.updated_commits = update_commits(
                tags_sha_dict, commits, unreleased_bool
            )


class TestUpdateCommits4:
    def test_no_released_commits(self):
        tags_sha_dict = cases["test case 4"]["tags_sha_dict"]
        commits = cases["test case 4"]["commits"]
        commits = make_commit_class(commits)
        unreleased_bool = cases["test case 4"]["unreleased_bool"]
        with pytest.raises(ValueError):
            self.updated_commits = update_commits(
                tags_sha_dict, commits, unreleased_bool
            )


class TestUpdateCommits5:
    def test_no_releases(self):
        tags_sha_dict = cases["test case 5"]["tags_sha_dict"]
        commits = cases["test case 5"]["commits"]
        commits = make_commit_class(commits)
        unreleased_bool = cases["test case 5"]["unreleased_bool"]
        with pytest.raises(ValueError):
            self.updated_commits = update_commits(
                tags_sha_dict, commits, unreleased_bool
            )
