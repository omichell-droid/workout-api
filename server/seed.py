from datetime import date

from app import app
from extensions import db
from models import Workout, Exercise, WorkoutExercise

with app.app_context():
    print("Deleting old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")
    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    push_up = Exercise(name="Push Up", category="strength", equipment_needed=False)
    run = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)
    plank = Exercise(name="Plank", category="balance", equipment_needed=False)
    stretch = Exercise(name="Hamstring Stretch", category="flexibility", equipment_needed=False)
    burpee = Exercise(name="Burpee", category="cardio", equipment_needed=False)    
    print("Creating workouts...")
    leg_day = Workout(date=date(2026, 11, 2), duration_minutes=60, notes="Leg day")
    upper_body = Workout(date=date(2026, 11, 4), duration_minutes=45, notes="Upper body")
    cardio_day = Workout(date=date(2026, 11, 6), duration_minutes=30, notes="Cardio")

    print("Adding exercises to workouts...")
    entries = [
        WorkoutExercise(workout=leg_day, exercise=squat, sets=5, reps=5),
        WorkoutExercise(workout=leg_day, exercise=stretch, duration_seconds=120),
        WorkoutExercise(workout=upper_body, exercise=push_up, sets=4, reps=15),
        WorkoutExercise(workout=upper_body, exercise=plank, duration_seconds=90),
        WorkoutExercise(workout=cardio_day, exercise=run, duration_seconds=1200),
    ]

    db.session.add_all([squat, push_up, run, plank, stretch])
    db.session.add_all([leg_day, upper_body, cardio_day])
    db.session.add_all(entries)
    db.session.commit()

    print("Done seeding!")