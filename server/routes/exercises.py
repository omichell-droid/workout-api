from flask import Blueprint, jsonify, request

from extensions import db
from models import Exercise
from schemas import ExerciseSchema

exercises_bp = Blueprint("exercises", __name__)


@exercises_bp.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(ExerciseSchema(many=True).dump(exercises)), 200


@exercises_bp.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(ExerciseSchema().dump(exercise)), 200


@exercises_bp.route("/exercises", methods=["POST"])
def create_exercise():
    data = ExerciseSchema().load(request.get_json())
    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    return jsonify(ExerciseSchema().dump(exercise)), 201


@exercises_bp.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return "", 204