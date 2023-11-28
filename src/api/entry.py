from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from src.api import user

router = APIRouter(
  prefix="/entry",
  tags=["entry"],
  dependencies=[Depends(user.authorize)],
)

class CreateGoalEntry(BaseModel):
  exercise_name: str
  goal_reps: int
  goal_weight: int

class EditGoalEntry(BaseModel):
  goal_reps: int
  goal_weight: int

@router.post("/{diary_id}/{day}")
def create_goal_entry(diary_id: int, day: str, entry: CreateGoalEntry, user=Depends(user.get_user)):
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
      entry_id = connection.execute(sqlalchemy.text("""
          INSERT INTO goalentry (day_id, exercise_id, goal_reps, goal_weight)
          SELECT :day_id, exercise.id, :goal_reps, :goal_weight
          FROM exercise
          WHERE name = :name
          RETURNING goalentry.id
          """), {"day_id": day_id, "name": entry.exercise_name, "goal_reps": entry.goal_reps, "goal_weight": entry.goal_weight}).scalar_one()  
    except NoResultFound:
      raise HTTPException(status_code=404, detail="An exercise with this name does not exist.")
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
          JOIN goalentry ON goalentry.day_id = day.id
          WHERE goalentry.id = :entry_id
      """), {"entry_id": entry_id}).scalar_one()
    except NoResultFound:
      raise HTTPException(status_code=404, detail="An entry with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You did not create this entry.")
    connection.execute(sqlalchemy.text("DELETE FROM goalentry WHERE id = :entry_id"), {"entry_id": entry_id})
  return f"Entry (id={entry_id}) successfully deleted."

@router.patch("/{entry_id}")
def edit_goal_entry(entry_id: int, entry: EditGoalEntry, user=Depends(user.get_user)):
  """Edit an entry that you created by id."""
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("""
          SELECT diary.owner
          FROM diary
          JOIN day ON day.diary_id = diary.id
          JOIN goalentry ON goalentry.day_id = day.id
          WHERE goalentry.id = :entry_id
      """), {"entry_id": entry_id}).scalar_one()
    except NoResultFound:
      raise HTTPException(status_code=404, detail="An entry with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You did not create this entry.")
    connection.execute(sqlalchemy.text("""
        UPDATE goalentry
        SET goal_reps = :goal_reps, goal_weight = :goal_weight
        WHERE id = :entry_id
        """), {"goal_reps": entry.goal_reps, "goal_weight": entry.goal_weight, "entry_id": entry_id})
  return {"edited_goal_reps": entry.goal_reps, "edited_goal_weight": entry.goal_weight}

#TODO: Get diary_id and day by entry
#TODO: all the endpoints for actualweight/reps, basically same thing but with diff table
#TODO get goalweigt and reps by entryid