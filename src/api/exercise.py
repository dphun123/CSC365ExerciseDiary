from fastapi import APIRouter, Depends, Request
from enum import Enum
import requests
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
import os
from src.api import user

router = APIRouter(
  prefix="/exercise",
  tags=["exercise"],
)

# Create a diary
@router.post("/")
def get_recommendation():

  # Get the exercise names for the day
@router.get("/{diary_id}/{day}")
def get_exercises_for_day(diary_id: int, day: str):
  exercise_names = []
  with db.engine.begin() as connection:
    exercises = connection.execute(sqlalchemy.text("""
        SELECT ex.name
        FROM entry en
        JOIN exercise ex ON en.exercise_id = ex.id
        JOIN day d ON en.day_id = d.id
        WHERE d.diary_id = :diary_id AND d.day_name = :day
        """), {"diary_id": diary_id, "day": day}).fetchall()
    for row in exercises:
      exercise_names.append(row.name)
  return exercise_names
