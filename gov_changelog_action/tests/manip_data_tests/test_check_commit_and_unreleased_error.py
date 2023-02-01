import pytest
from gov_changelog_action.src.manip_data import check_commit_and_unreleased_error


class TestCheckCommitUnreleaseedError:
    def test_unreleased_bool_true(self):
        assert check_commit_and_unreleased_error("true", {}) == "Unreleased"
        assert check_commit_and_unreleased_error("TrUe", {}) == "Unreleased"

    def test_unreleased_bool_false(self):
        assert check_commit_and_unreleased_error("false", {"tag": "sha"}) == "tag"
        assert check_commit_and_unreleased_error("FaLsE", {"tag": "sha"}) == "tag"

    def test_no_tags_sha(self):
        with pytest.raises(ValueError):
            check_commit_and_unreleased_error("FaLsE", {})

    def test_bad_input(self):
        with pytest.raises(ValueError):
            check_commit_and_unreleased_error("Bool", {})
