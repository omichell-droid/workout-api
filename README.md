# Workout Tracker API

A Flask REST API for personal trainers to track workouts and exercises. Exercises are reusable and can be added to many workouts, with sets, reps or a duration for each.

## Models
- **Workout**: date, duration_minutes, notes
- **Exercise**: name (unique), category, equipment_needed
- **WorkoutExercise** (join table): workout_id, exercise_id, reps, sets, duration_seconds

A workout has many exercises through WorkoutExercise, and an exercise can belong to many workouts. Deleting a workout or exercise also deletes its WorkoutExercise rows.

## Validations
- **Table constraints:** duration_minutes > 0, unique exercise name, required columns (NOT NULL), foreign keys
- **Model validations:** duration must be more than 0; category must be strength, cardio, flexibility or balance
- **Schema validations:** required fields, name length 2–100, allowed categories, duration 1–600, notes up to 500 characters, and an exercise entry needs reps and sets, or duration_seconds

## Installation
```bash
pipenv install
pipenv shell
cd server
export FLASK_APP=app.py
flask db upgrade
python seed.py
```

## Running the App
```bash
cd server
flask run --port 5555
```

## Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show one workout with its exercises |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show one exercise with the workouts it's in |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

### Example request bodies
POST `/workouts`
```json
{ "date": "2026-11-20", "duration_minutes": 45, "notes": "Leg day" }
```
POST `/workouts/1/exercises/2/workout_exercises`
```json
{ "sets": 3, "reps": 10 }
```