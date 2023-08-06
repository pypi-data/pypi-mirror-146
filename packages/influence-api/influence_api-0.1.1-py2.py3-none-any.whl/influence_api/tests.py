import os

import pytest

from . import InfluenceClient
from .client import INFLUENCE_CLIENT_ID, INFLUENCE_CLIENT_SECRET

SKIP_LIVE_TESTS = INFLUENCE_CLIENT_ID is None or INFLUENCE_CLIENT_SECRET is None

live_test = pytest.mark.skipif(
    SKIP_LIVE_TESTS, reason="no available live API credentials"
)


@pytest.fixture(scope="session")
def influence_client():
    return InfluenceClient()


def test_init():
    _ = InfluenceClient(refresh_token=False)


@live_test
def test_fetch_asteroid(influence_client: InfluenceClient):
    assert influence_client.get_asteroid(1)["name"] == "TG-29980 'Adalia Prime'"


@live_test
def test_fetch_crewmate(influence_client: InfluenceClient):
    assert influence_client.get_crewmate(1)["name"] == "Scott Manley"
