import copy
import pytest
from src import app


@pytest.fixture(autouse=True)
def reset_activities():
    initial_activities = copy.deepcopy(app.activities)
    yield
    app.activities.clear()
    app.activities.update(copy.deepcopy(initial_activities))
