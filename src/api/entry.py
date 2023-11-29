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

class GoalEntry(BaseModel):
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
def create_entry(diary_id: int, day: str, entry: GoalEntry, user=Depends(user.get_user)):
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
          INSERT INTO entry (day_id, exercise, goal_reps, goal_weight)
          VALUES (:day_id, :exercise, :goal_reps, :goal_weight)
          RETURNING id
          """), {"day_id": day_id, "exercise": entry.exercise, "goal_reps": entry.goal_reps, "goal_weight": entry.goal_weight}).scalar_one()  
    except IntegrityError:
      raise HTTPException(status_code=404, detail="An exercise with this name does not exist. View possible exercises with the exercises endpoint.")
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
  """Edit an entry that you created by id. Delete any values you do not want updated."""
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
      set_clause = ", ".join([f"{key} = :{key}" for key, value in edit_entry.dict().items() if value is not None])
      connection.execute(sqlalchemy.text(f"""
          UPDATE entry
          SET {set_clause}
          WHERE id = :entry_id
          """), {"entry_id": entry_id, **edit_entry.dict()})
    except IntegrityError:
      raise HTTPException(status_code=404, detail="An exercise with this name does not exist. View possible exercises with the exercises endpoint.")
  return {"entry_id": entry_id, **edit_entry.dict()}

#TODO: Get diary_id and day by entry