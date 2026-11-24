from flask import Blueprint, jsonify, request

from extensions import db
from models import Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, WorkoutExerciseSchema

workouts_bp = Blueprint("workouts", __name__)


@workouts_bp.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(WorkoutSchema(many=True).dump(workouts)), 200


@workouts_bp.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(WorkoutSchema().dump(workout)), 200


@workouts_bp.route("/workouts", methods=["POST"])
def create_workout():
    data = WorkoutSchema().load(request.get_json())
    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return jsonify(WorkoutSchema().dump(workout)), 201


@workouts_bp.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return "", 204


@workouts_bp.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if workout is None or exercise is None:
        return jsonify({"error": "Workout or exercise not found"}), 404

    data = WorkoutExerciseSchema().load(request.get_json())
    workout_exercise = WorkoutExercise(workout=workout, exercise=exercise, **data)
    db.session.add(workout_exercise)
    db.session.commit()
    return jsonify(WorkoutExerciseSchema().dump(workout_exercise)), 201