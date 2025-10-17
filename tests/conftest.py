import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    # Provide a TestClient and reset in-memory activities before each test
    # Copy original participants to restore state if needed
    # We'll deep copy the activities dict so mutations don't leak across tests
    import copy

    original = copy.deepcopy(activities)
    with TestClient(app) as c:
        yield c

    # restore
    activities.clear()
    activities.update(original)
