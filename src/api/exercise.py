from fastapi import APIRouter, Query
from enum import Enum
from typing import List, Union
import sqlalchemy
from src import database as db

router = APIRouter(
  prefix="/exercise",
  tags=["exercise"],
)

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"   

class MuscleOptions(str, Enum):
  chest = "Chest"
  forearms = "Forearms"
  lats = "Lats"
  middle_back = "Middle Back"
  lower_back = "Lower Back"
  neck = "Neck"
  quadriceps = "Quadriceps"
  hamstrings = "Hamstrings"
  calves = "Calves"
  triceps = "Triceps"
  traps = "Traps"
  shoulders = "Shoulders"
  abdominals = "Abdominals"
  glutes = "Glutes"
  biceps = "Biceps"
  adductors = "Adductors"
  abductors = "Abductors"

class TypeOptions(str, Enum):
  cardio = "Cardio"
  olympic_weightlifting = "Olympic Weightlifting"
  plyometrics = "Plyometrics"
  powerlifting = "Powerlifting"
  strength = "Strength"
  stretching = "Stretching"
  strongman = "Strongman"

class EquipmentOptions(str, Enum):
  bands = "Bands"
  foam_roll = "Foam Roll"
  barbell = "Barbell"
  kettlebells = "Kettlebells"
  body_only = "Body Only"
  machine = "Machine"
  cable = "Cable"
  medicine_ball = "Medicine Ball"
  dumbbell = "Dumbbell"
  none_equipment = "None"
  e_z_curl_bar = "E-Z Curl Bar"
  other = "Other"
  exercise_ball = "Exercise Ball"

class LevelOptions(str, Enum):
  beginner = "Beginner"
  intermediate = "Intermediate"
  expert = "Expert"

#TODO: Get the exercise names for the day
# @router.get("/{diary_id}/{day}")
# def get_exercises_for_day(diary_id: int, day: str):
#   exercise_names = []
#   with db.engine.begin() as connection:
#     exercises = connection.execute(sqlalchemy.text("""
#         SELECT ex.name
#         FROM entry en
#         JOIN exercise ex ON en.exercise_id = ex.id
#         JOIN day d ON en.day_id = d.id
#         WHERE d.diary_id = :diary_id AND d.day_name = :day
#         """), {"diary_id": diary_id, "day": day}).fetchall()
#     for row in exercises:
#       exercise_names.append(row.name)
#   return exercise_names

@router.get("/search/")
def search_exercises(
  exercise: str = "",
  sort_order_by_rating: SortOrder = SortOrder.desc,
  muscle: List[MuscleOptions] = Query(None),
  type: List[TypeOptions] = Query(None),
  equipment: List[EquipmentOptions] = Query(None),
  level: List[LevelOptions] = Query(None),
  count: Union[None, int] = Query(None, gt=0),
):
  with db.engine.begin() as connection:
    where_conditions = []
    params = {}
    if exercise:
      where_conditions.append("exercise.name ILIKE :exercise")
      params["exercise"] = f"%{exercise}%"
    if muscle:
      where_conditions.append("exercise.muscle IN :muscle")
      params["muscle"] = tuple(m.value for m in muscle)
    if type:
      where_conditions.append("exercise.type IN :type")
      params["type"] = tuple(t.value for t in type)
    if equipment:
      where_conditions.append("exercise.equipment IN :equipment")
      params["equipment"] = tuple(e.value for e in equipment)
    if level:
      where_conditions.append("exercise.level IN :level")
      params["level"] = tuple(l.value for l in level)

    where_clause = " AND ".join(where_conditions)
    where_clause = f"WHERE {where_clause}" if where_clause else ""
    limit_clause = f"LIMIT :count" if count else ""

    exercises = connection.execute(sqlalchemy.text(f"""
        SELECT *
        FROM exercise
        {where_clause}
        ORDER BY rating {sort_order_by_rating}
        {limit_clause}
        """), params).fetchall()
    
  results = []
  for exercise in exercises:
    results.append({
        "name": exercise.name,
        "rating": exercise.rating,
        "muscle": exercise.muscle,
        "type": exercise.type,
        "equipment": exercise.equipment,
        "level": exercise.level,
        "instructions": exercise.instructions
    })
  return results