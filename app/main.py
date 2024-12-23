from flask import Flask, jsonify, request
from os import environ

from app.config import Config
from app.database import add_to_db, db
from app.logic import calculate_unique_coordinates
from app.models import Execution


def initialize_app():
    """Initialize SQLAlchemy with `app`."""
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config())
    db.init_app(flask_app)
    return flask_app


app = initialize_app()


@app.route("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/tibber-developer-test/enter-path", methods=["POST"])
def tibber_developer_test():

    # Fetch data from POST data without input validation
    request_data = request.get_json()
    start_point = (request_data["start"]["x"], request_data["start"]["y"])
    commands = request_data["commands"]

    # Main logic to calculate unique places and duration
    result, duration = calculate_unique_coordinates(start_point, commands)
    new_execution = Execution(commands=len(commands), result=result, duration=duration)
    result = add_to_db(new_execution)

    # Return the resulting document or an error
    return (jsonify(result), 200) if result else (jsonify({"error": "request failed"}), 500)


if __name__ == "__main__":

    # For non-prod environments, initialize the local database
    if environ.get("ENV") != "prod":
        with app.app_context():
            db.create_all()

    app.run(host="0.0.0.0", port=5000)
