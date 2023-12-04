from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from typing import Union, Optional
from pydantic import BaseModel
import sqlalchemy
from src import database as db
from src.api import user

router = APIRouter(
  prefix="/entry",
  tags=["entry"],
  dependencies=[Depends(user.authorize)],
)

class CreateEntry(BaseModel):
  exercise: str
  goal_reps: int
  goal_weight: int

class EditEntry(BaseModel):
  exercise: Optional[str]
  goal_reps: Optional[int]
  goal_weight: Optional[int]
  reps: Optional[int]
  weight: Optional[int]
  comments: Optional[str]

@router.post("/{diary_id}/{day}")
def create_entry(diary_id: int, day: str, entry: CreateEntry, user=Depends(user.get_user)):
  """Add a goal entry in a specific diary and for a specific day."""
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).scalar_one()
    except NoResultFound:
      raise HTTPException(status_code=404, detail="A diary with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You do not own this diary.")
    try:
      day_id = connection.execute(sqlalchemy.text("""
          SELECT id
          FROM day
          WHERE diary_id = :diary_id AND day_name = :day
          """), {"diary_id": diary_id, "day": day}).scalar_one()
    except NoResultFound:
      raise HTTPException(status_code=404, detail="This combination of diary and day id's does not exist.")
    try:
      exercise_name = connection.execute(sqlalchemy.text("""
          SELECT name
          FROM exercise
          WHERE name ILIKE :exercise
          """), {"exercise": entry.exercise}).scalar_one()
      entry_id = connection.execute(sqlalchemy.text("""
        INSERT INTO entry (day_id, exercise, goal_reps, goal_weight)
        VALUES (:day_id, :exercise, :goal_reps, :goal_weight)
        RETURNING id
        """), {"day_id": day_id, "exercise": exercise_name, "goal_reps": entry.goal_reps, "goal_weight": entry.goal_weight}).scalar_one()  
    except:
      exercises = connection.execute(sqlalchemy.text("""
          SELECT name
          FROM exercise
          WHERE name ILIKE :exercise
          """), {"exercise": f"%{entry.exercise}%"}).scalars()
      exercises = ', '.join(exercises)
      if exercises:
        raise HTTPException(status_code=404, detail=f"Exercise not found. Did you mean one of these: {exercises}?")
      else:
        raise HTTPException(status_code=404, detail="An exercise with this name (or similar) does not exist. View possible exercises with the exercises endpoint.")
  return {"entry_id": entry_id}

@router.delete("/{entry_id}")
def delete_entry(entry_id: int, user=Depends(user.get_user)):
  """Delete an entry that you created by id."""
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("""
          SELECT diary.owner
          FROM diary
          JOIN day ON day.diary_id = diary.id
          JOIN entry ON entry.day_id = day.id
          WHERE entry.id = :entry_id
      """), {"entry_id": entry_id}).scalar_one()
    except NoResultFound:
      raise HTTPException(status_code=404, detail="An entry with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You did not create this entry.")
    connection.execute(sqlalchemy.text("DELETE FROM entry WHERE id = :entry_id"), {"entry_id": entry_id})
  return f"Entry (id={entry_id}) successfully deleted."

@router.patch("/{entry_id}")
def edit_entry(entry_id: int, edit_entry: EditEntry = Body(None, embed=True), user=Depends(user.get_user)):
  """Edit an entry that you created by id. Default values will not lead to updates."""
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("""
          SELECT diary.owner
          FROM diary
          JOIN day ON day.diary_id = diary.id
          JOIN entry ON entry.day_id = day.id
          WHERE entry.id = :entry_id
      """), {"entry_id": entry_id}).scalar_one()
    except NoResultFound:
      raise HTTPException(status_code=404, detail="An entry with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You did not create this entry.")
    if all(value is None for value in edit_entry.dict().values()):
      raise HTTPException(status_code=422, detail="At least one value must be edited.")
    try:
      filtered_entry = {key: value for key, value in edit_entry.dict().items() if value not in (0, "string")}
      print(filtered_entry)
      if 'exercise' in filtered_entry:
        exercise_name = connection.execute(sqlalchemy.text("""
            SELECT name
            FROM exercise
            WHERE name ILIKE :exercise
            """), {"exercise": filtered_entry['exercise']}).scalar_one()
        filtered_entry['exercise'] = exercise_name
      set_clause = ", ".join([f"{key} = :{key}" for key, value in filtered_entry.items() if value is not None])
      connection.execute(sqlalchemy.text(f"""
          UPDATE entry
          SET {set_clause}
          WHERE id = :entry_id
          """), {"entry_id": entry_id, **filtered_entry})
    except:
      exercises = connection.execute(sqlalchemy.text("""
          SELECT name
          FROM exercise
          WHERE name ILIKE :exercise
          """), {"exercise": f"%{filtered_entry['exercise']}%"}).scalars()
      exercises = ', '.join(exercises)
      if exercises:
        raise HTTPException(status_code=404, detail=f"Exercise not found. Did you mean one of these: {exercises}?")
      else:
        raise HTTPException(status_code=404, detail="An exercise with this name (or similar) does not exist. View possible exercises with the exercises endpoint.")
  return {"entry_id": entry_id, **filtered_entry}

@router.get("/diary-day/{entry_id}")
def get_diary_and_day_by_entry(entry_id: int, user=Depends(user.get_user)):
  """Get the diary id and day that an entry belongs to."""
  with db.engine.begin() as connection:
    diary = connection.execute(sqlalchemy.text("""
        SELECT diary.owner, diary.id, day.day_name
        FROM diary
        JOIN day ON day.diary_id = diary.id
        JOIN entry ON entry.day_id = day.id
        WHERE entry.id = :entry_id
        """), {"entry_id": entry_id}).fetchone()
    if not diary:
      raise HTTPException(status_code=404, detail="An entry with this id does not exist.")
    if diary.owner != user:
      raise HTTPException(status_code=401, detail="You did not create this entry.")
  return {"diary_id": diary.id, "day_name": diary.day_name}