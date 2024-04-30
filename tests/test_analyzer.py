import json

import pytest

from data_analyzer import DataAnalyzer


@pytest.mark.parametrize("test_input,expected",
[({"data": {"privacy": {"isPrivacyModeEnabled": True}}}, True),
 ({"data": {"privacy": {"isPrivacyModeEnabled": False}}}, False)])
def test_compliance_with_gdpr(test_input, expected):
    assert DataAnalyzer().is_compliant_with_GDPR(test_input) == expected

def test_counting_harsh_braking_events():
    with open('../data/trip_data.json') as f:
        trip_data = json.load(f)

        assert DataAnalyzer().count_harsh_braking_events(trip_data) == 6




