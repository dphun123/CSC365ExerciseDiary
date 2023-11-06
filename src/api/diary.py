from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
  prefix="/diary",
  tags=["diary"],
  dependencies=[Depends(auth.get_api_key)],
)

# Create a diary
@router.post("/")
def create_diary(days: list[str]):
  with db.engine.begin() as connection:
    diary_id = connection.execute(sqlalchemy.text("INSERT INTO diary DEFAULT VALUES RETURNING id")).first().id
    for day_name in days:
      connection.execute(sqlalchemy.text("""
        INSERT INTO day (day_name, diary_id)
        VALUES (:day_name, :diary_id)
        """), {"day_name": day_name, "diary_id": diary_id})
  return diary_id

# Delete a diary
@router.delete("/{diary_id}")
def delete_diary(diary_id: int):
  with db.engine.begin() as connection:
    connection.execute(sqlalchemy.text("DELETE FROM diary WHERE id = :diary_id"), {"diary_id": diary_id})
  return "OK"

class EditEntry(BaseModel):
  reps: int
  weight: int
  comments: str

class CreateEntry(BaseModel):
  exercise_name: str
  goal_reps: int
  goal_weight: int

# Add an entry in a diary
@router.post("/{diary_id}/{day}")
def add_entry(diary_id: int, day: str, entry: CreateEntry):
  with db.engine.begin() as connection:
    day_id = connection.execute(sqlalchemy.text("""
        SELECT id
        FROM day
        WHERE diary_id = :diary_id AND day_name = :day
        """), {"diary_id": diary_id, "day": day}).first().id
    exercise_id = connection.execute(sqlalchemy.text("""
        SELECT id
        FROM exercise
        WHERE name = :name
        """), {"name": entry.exercise_name}).first().id
    entry_id = connection.execute(sqlalchemy.text("""
        INSERT INTO entry (day_id, exercise_id, goal_reps, goal_weight)
        VALUES (:day_id, :exercise_id, :goal_reps, :goal_weight)
        RETURNING id
        """), {"day_id": day_id, "exercise_id": exercise_id, "goal_reps": entry.goal_reps, "goal_weight": entry.goal_weight}).first().id
  return entry_id

# Edit an entry in a diary
@router.post("/{entry_id}")
def edit_entry(entry_id: int, entry: EditEntry):
  with db.engine.begin() as connection:
    connection.execute(sqlalchemy.text("""
        UPDATE entry
        SET reps = :reps, weight = :weight, comments = :comments
        WHERE id = :entry_id
        """), {"reps": entry.reps, "weight": entry.weight, "comments": entry.comments, "entry_id": entry_id})
  return "OK"

# Get the exercise names for the day
@router.get("/{diary_id}/{day}")
def get_exercises_for_day(diary_id: int, day: str):
  exercise_names = []
  with db.engine.begin() as connection:
    exercises = connection.execute(sqlalchemy.text("""
        WITH get_day_id AS (
          SELECT id
          FROM day
          WHERE diary_id = :diary_id AND day_name = :day
        )
        SELECT ex.name
        FROM entry en
        JOIN exercise ex ON en.exercise_id = ex.id
        JOIN get_day_id gdi ON en.day_id = gdi.id
        """), {"diary_id": diary_id, "day": day}).fetchall()
    for row in exercises:
      exercise_names.append(row.name)
  return exercise_names