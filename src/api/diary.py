from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
import sqlalchemy
from src import database as db
from src.api import user

router = APIRouter(
  prefix="/diary",
  tags=["diary"],
  dependencies=[Depends(user.authorize)],
)

@router.post("/")
def create_diary(days: list[str], user=Depends(user.get_user)):
  """Create a diary."""
  if len(days) == 0:
    raise HTTPException(status_code=422, detail="Your diary must contain at least one day.")
  with db.engine.begin() as connection:
    diary_id = connection.execute(sqlalchemy.text("INSERT INTO diary(owner) VALUES (:user) RETURNING id"), {"user": user}).scalar_one()
    for day_name in days:
      connection.execute(sqlalchemy.text("""
          INSERT INTO day (day_name, diary_id)
          VALUES (:day_name, :diary_id)
          """), {"day_name": day_name, "diary_id": diary_id})
  return {"diary_id": diary_id}

@router.delete("/{diary_id}")
def delete_diary(diary_id: int, user=Depends(user.get_user)):
  """Delete a diary that you own by id."""
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).scalar_one()
    except NoResultFound:
      raise HTTPException(status_code=404, detail="A diary with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You do not own this diary.")
    connection.execute(sqlalchemy.text("DELETE FROM diary WHERE id = :diary_id"), {"diary_id": diary_id})
  return f"Diary (id={diary_id}) successfully deleted."

#TODO: need to add entries and comments
# @router.get("/")
# def get_all_diaries(user=Depends(user.get_user)):
#   """Get the list of diaries you own, along with their corresponding days, exercises, and entries."""
#   diary_list = []
#   with db.engine.begin() as connection:
#     diary_days = connection.execute(sqlalchemy.text("""
#         SELECT diary.id, day.day_name
#         FROM diary
#         JOIN day ON day.diary_id = diary.id
#         WHERE owner = :user
#         """), {"user": user}).fetchall()
#     for diary_day in diary_days:
#       existing_diary = next((d for d in diary_list if d['diary_id'] == diary_day.id), None)
#       if existing_diary is None:
#         diary_list.append({"diary_id": diary_day.id, "days": []})
#       current_diary = next(d for d in diary_list if d['diary_id'] == diary_day.id)
#       current_diary["days"].append(diary_day.day_name)
#   if len(diary_list) == 0:
#     return "You have no diaries."
#   return diary_list

@router.get("/{diary_id}")
def get_diary(diary_id: int, user=Depends(user.get_user)):
  """Get a specific diary that you own by id, along with its corresponding days."""
  days = []
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).scalar_one()
    except NoResultFound:
      raise HTTPException(status_code=404, detail="A diary with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You do not own this diary.")
    diary = connection.execute(sqlalchemy.text("""
        SELECT diary.id, day.day_name
        FROM diary
        JOIN day ON day.diary_id = diary.id
        WHERE diary.id = :diary_id AND owner = :user
        """), {"diary_id": diary_id, "user": user}).fetchall()
    for day in diary:
      days.append(day.day_name)
  return {"diary_id": diary_id, "days": days}

#TODO: Get exercises and all entries/comments for day
# @router.get("/{diary_id}/{day}")
# def get_diary_day(diary_id: int, day: str):
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

#TODO: Get exercises and goals for day
# @router.get("/{diary_id}/{day}/plan")
# def get_diary_day(diary_id: int, day: str):