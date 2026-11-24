from sqlalchemy.orm import validates
from extensions import db


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    # Table constraint: duration must be more than 0
    duration_minutes = db.Column(db.Integer, db.CheckConstraint("duration_minutes > 0", name="duration_positive"), nullable=False)
    notes = db.Column(db.Text)

    # One workout has many workout_exercises
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

    # Model validation
    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be more than 0")
        return value


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    # Table constraint: name must be unique
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # One exercise has many workout_exercises
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")

    # Model validation
    @validates("category")
    def validate_category(self, key, value):
        if value not in ["strength", "cardio", "flexibility", "balance"]:
            raise ValueError("Category must be strength, cardio, flexibility or balance")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)