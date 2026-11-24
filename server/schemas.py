from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(["strength", "cardio", "flexibility", "balance"]))
    equipment_needed = fields.Bool()
    workout_exercises = fields.Nested("WorkoutExerciseSchema", many=True, exclude=("exercise",), dump_only=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1))
    sets = fields.Int(validate=validate.Range(min=1))
    duration_seconds = fields.Int(validate=validate.Range(min=1))
    exercise = fields.Nested(ExerciseSchema, exclude=("workout_exercises",), dump_only=True)

    @validates_schema
    def check_reps_sets_or_duration(self, data, **kwargs):
        has_reps_and_sets = data.get("reps") and data.get("sets")
        has_duration = data.get("duration_seconds")
        if not has_reps_and_sets and not has_duration:
            raise ValidationError("Give reps and sets, or duration_seconds")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(validate=validate.Length(max=500))
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)