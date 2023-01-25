import pytest
import json
from gov_changelog_action.src.manip_data import get_prefixes

cases = json.load(
    open("gov_changelog_action/tests/manip_data_tests/get_prefixes_testcase.json")
)


@pytest.fixture
def test_case_1():
    config = cases["test case 1"]
    unique_prefixes = get_prefixes(config)

    return unique_prefixes


class TestGetPrixes1:
    def test_number_prefixes_shown(self, test_case_1):
        assert len(test_case_1) == 2

    def test_header_prefix(self, test_case_1):
        assert (
            test_case_1[0].heading == cases["test case 1"]["prefixes"]["add"]["heading"]
        )
        assert (
            test_case_1[1].heading == cases["test case 1"]["prefixes"]["fix"]["heading"]
        )

    def test_release_bump(self, test_case_1):
        assert (
            test_case_1[0].version_bump
            == cases["test case 1"]["prefixes"]["add"]["release"]
        )
        assert (
            test_case_1[1].version_bump
            == cases["test case 1"]["prefixes"]["fix"]["release"]
        )
