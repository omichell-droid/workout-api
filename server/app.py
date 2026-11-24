from flask import Flask, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from extensions import db, migrate
import models
from routes.workouts import workouts_bp
from routes.exercises import exercises_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(workouts_bp)
app.register_blueprint(exercises_bp)


# Schema validation failed (bad JSON sent by the user)
@app.errorhandler(ValidationError)
def handle_schema_error(error):
    return jsonify({"errors": error.messages}), 400


# Model validation failed (@validates raised ValueError)
@app.errorhandler(ValueError)
def handle_model_error(error):
    db.session.rollback()
    return jsonify({"errors": [str(error)]}), 400


# Table constraint failed (e.g. duplicate exercise name)
@app.errorhandler(IntegrityError)
def handle_database_error(error):
    db.session.rollback()
    return jsonify({"errors": ["Database constraint failed"]}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)