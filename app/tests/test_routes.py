import pytest
from flask import json
from app.main import app, db
from app.models import Execution


@pytest.fixture
def client():
    """Fixture to create a test client and set up a test database."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db/apidb"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def _get_response_data(client, payload):
    """
    Small helper function to fetch the payload and check the response and whether
    that response is also in the database.
    """

    # Fetch POST response from the endpoint
    response = client.post(
        "/tibber-developer-test/enter-path",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200

    # Verify the response contains the correct structure
    data = response.json
    assert "id" in data
    assert data["commands"] == len(payload["commands"])
    assert "result" in data
    assert "duration" in data

    # Return the JSON data
    return data


def test_simple_execution(client):
    """Test the response of POST endpoint and if entry is in database."""

    # Fetch response data
    data = _get_response_data(client, {
        "start": {"x": 0, "y": 0},
        "commands": [{"direction": "north", "steps": 1}]
    })

    # Verify the database has the entry
    with app.app_context():
        execution = Execution.query.session.get(Execution, data["id"])
        assert execution is not None
        assert execution.id == data["id"]
        assert execution.commands == data["commands"]
        assert execution.result == data["result"]
        assert execution.duration == data["duration"]


def test_assignment_example(client):
    """Test the example from the assignment."""

    # Fetch response data
    data = _get_response_data(client, {
        "start": {"x": 10, "y": 22},
        "commands": [
            {"direction": "east", "steps": 2},
            {"direction": "north", "steps": 1},
        ]
    })

    # Verify the database has the entry and that the data matches
    # expectation (commands = 2, result = 4)
    with app.app_context():
        execution = Execution.query.session.get(Execution, data["id"])
        assert execution is not None
        assert execution.id == data["id"]
        assert execution.commands == data["commands"]
        assert execution.commands == 2
        assert execution.result == data["result"]
        assert execution.result == 4
        assert execution.duration == data["duration"]


def test_running_in_circles(client):
    """
    Similar test as in `test_logic`, to see if running in circles 100 times
    only yields a response of 4 cleaned coordinates.
    """

    # Fetch response data
    data = _get_response_data(client, {
        "start": {"x": 1, "y": 1},
        "commands": [
            {"direction": "east", "steps": 1},
            {"direction": "north", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "south", "steps": 1},
        ] * 100
    })

    # Verify the database has the entry and that the data matches
    # expectation (commands = 400, result = 4)
    with app.app_context():
        execution = Execution.query.session.get(Execution, data["id"])
        assert execution is not None
        assert execution.id == data["id"]
        assert execution.commands == data["commands"]
        assert execution.commands == 400
        assert execution.result == data["result"]
        assert execution.result == 4
        assert execution.duration == data["duration"]


def test_running_maximum_commands(client):
    """
    Test to verify performance when running 10,000 commands with maximum
    amount of steps (99,999).
    """

    # Fetch response data
    data = _get_response_data(client, {
        "start": {"x": -100000, "y": -100000},
        "commands": [
            {"direction": "east", "steps": 99999},
            {"direction": "north", "steps": 99999},
            {"direction": "west", "steps": 99998},
            {"direction": "south", "steps": 99998},
        ] * 2500
    })

    # Verify the database has the entry and that it runs within 10s
    with app.app_context():
        execution = Execution.query.session.get(Execution, data["id"])
        assert execution is not None
        assert execution.id == data["id"]
        assert execution.commands == data["commands"]
        assert execution.commands == 10000
        assert execution.result == data["result"]
        assert execution.result == 993737501
        assert execution.duration < 10
