from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
import sqlalchemy
from src import pt_database as db
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
  unique_day_names = []
  for day in days:
    if day in unique_day_names:
      raise HTTPException(status_code=422, detail=f"Duplicate day name found: {day}.")
    unique_day_names.append(day)
  with db.engine.begin() as connection:
    diary_id = connection.execute(sqlalchemy.text("INSERT INTO diary(owner) VALUES (:user) RETURNING id"), {"user": user}).scalar_one()
    explain = connection.execute(sqlalchemy.text("EXPLAIN ANALYZE INSERT INTO diary(owner) VALUES (:user)"), {"user": user}).fetchall()
    for row in explain:
      print(row)
    values = [{"day_name": day, "diary_id": diary_id} for day in days]
    explain2 = connection.execute(sqlalchemy.text("""
        EXPLAIN ANALYZE
        INSERT INTO day (day_name, diary_id)
        VALUES (:day_name, :diary_id)
        """), values).fetchall()
    for row in explain2:
      print(row)
  return {"diary_id": diary_id}

#TODO: add sharing/unsharing diaries

@router.delete("/{diary_id}")
def delete_diary(diary_id: int, user=Depends(user.get_user)):
  """Delete a diary that you own by id."""
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).scalar_one()
      explain = connection.execute(sqlalchemy.text("EXPLAIN ANALYZE SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).fetchall()
      for row in explain:
        print(row)
    except NoResultFound:
      raise HTTPException(status_code=404, detail="A diary with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You do not own this diary.")
    explain2 = connection.execute(sqlalchemy.text("EXPLAIN ANALYZE DELETE FROM diary WHERE id = :diary_id"), {"diary_id": diary_id})
    for row in explain2:
      print(row)
  return f"Diary (id={diary_id}) successfully deleted."

@router.get("/all")
def get_all_diaries(user=Depends(user.get_user)):
  """Get the list of diaries you own, along with their corresponding days, exercises, and entries."""
  diary_list = []
  with db.engine.begin() as connection:
    diaries = connection.execute(sqlalchemy.text("""
        SELECT diary.id AS diary_id, diary.created_at diary_creation, day.day_name, entry.exercise,
            entry.id AS entry_id, entry.created_at entry_creation, goal_reps, goal_weight, reps, weight, comments
        FROM diary
        LEFT JOIN day ON day.diary_id = diary.id
        LEFT JOIN entry ON entry.day_id = day.id
        WHERE owner = :user
        ORDER BY diary.id, day.id, entry.id
        """), {"user": user}).fetchall()
    explain = connection.execute(sqlalchemy.text("""
        EXPLAIN ANALYZE
        SELECT diary.id AS diary_id, diary.created_at diary_creation, day.day_name, entry.exercise,
            entry.id AS entry_id, entry.created_at entry_creation, goal_reps, goal_weight, reps, weight, comments
        FROM diary
        LEFT JOIN day ON day.diary_id = diary.id
        LEFT JOIN entry ON entry.day_id = day.id
        WHERE owner = :user
        ORDER BY diary.id, day.id, entry.id
        """), {"user": user}).fetchall()
    for row in explain:
        print(row)
    for diary in diaries:
      existing_diary = next((d for d in diary_list if d['diary_id'] == diary.diary_id), None)
      if existing_diary is None:
        diary_list.append({"diary_id": diary.diary_id, "created_at": diary.diary_creation, "days": []})
      current_diary = next(d for d in diary_list if d['diary_id'] == diary.diary_id)
      day = next((d for d in current_diary["days"] if d["day_name"] == diary.day_name), None)
      if day is None:
        day = {"day_name": diary.day_name, "entries": []}
        current_diary["days"].append(day)
      if diary.exercise:
        day["entries"].append({"entry_id": diary.entry_id, "created_at": diary.entry_creation, "exercise": diary.exercise, "goal_reps": diary.goal_reps,
            "goal_weight": diary.goal_weight, "reps": diary.reps, "weight": diary.weight, "comments": diary.comments})
  if len(diary_list) == 0:
    raise HTTPException(status_code=404, detail="You have no diaries.")
  return diary_list

@router.get("/{diary_id}")
def get_diary(diary_id: int, user=Depends(user.get_user)):
  """Get a specific diary that you own by id, along with its corresponding days."""
  days = []
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).scalar_one()
      explain = connection.execute(sqlalchemy.text("EXPLAIN ANALYZE SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).fetchall()
      for row in explain:
        print(row)
    except NoResultFound:
      raise HTTPException(status_code=404, detail="A diary with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You do not own this diary.")
    diary = connection.execute(sqlalchemy.text("""
        SELECT diary.id, day.day_name
        FROM diary
        JOIN day ON day.diary_id = diary.id
        WHERE diary.id = :diary_id AND owner = :user
        ORDER BY day.id
        """), {"diary_id": diary_id, "user": user}).fetchall()
    explain2 = connection.execute(sqlalchemy.text("""
        EXPLAIN ANALYZE
        SELECT diary.id, day.day_name
        FROM diary
        JOIN day ON day.diary_id = diary.id
        WHERE diary.id = :diary_id AND owner = :user
        ORDER BY day.id
        """), {"diary_id": diary_id, "user": user}).fetchall()
    for row in explain2:
        print(row)
    for day in diary:
      days.append(day.day_name)
  return {"diary_id": diary_id, "days": days}

@router.get("/all/{diary_id}/{day}")
def get_diary_day(diary_id: int, day: str, user=Depends(user.get_user)):
    """Get the corresponding exercises and entries for a specific day in a specific diary."""
    entry_list = []
    with db.engine.begin() as connection:
      try:
        owner = connection.execute(sqlalchemy.text("SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).scalar_one()
        explain = connection.execute(sqlalchemy.text("EXPLAIN ANALYZE SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).fetchall()
        for row in explain:
          print(row)
      except NoResultFound:
        raise HTTPException(status_code=404, detail="A diary with this id does not exist.")
      if owner != user:
        raise HTTPException(status_code=401, detail="You do not own this diary.")
      entries = connection.execute(sqlalchemy.text("""
          SELECT diary.id AS diary_id, diary.created_at diary_creation, day.day_name, entry.id AS entry_id, entry.exercise,
              entry.goal_reps, entry.goal_weight, entry.reps, entry.weight, entry.comments, entry.created_at entry_creation
          FROM diary
          LEFT JOIN day ON day.diary_id = diary.id
          LEFT JOIN entry ON entry.day_id = day.id
          WHERE owner = :user AND diary_id = :diary_id AND day_name = :day
          ORDER BY entry.id
          """), {"user": user, "diary_id": diary_id, "day": day}).fetchall()
      explain2 = connection.execute(sqlalchemy.text("""
          DROP INDEX idx_day_diary_day_id, idx_entry_ranking;
          CREATE INDEX idx_day_diary_day_id ON day (diary_id, day_name);
          CREATE INDEX idx_entry_ranking ON entry (day_id, exercise, created_at DESC);
          EXPLAIN ANALYZE
          SELECT diary.id AS diary_id, diary.created_at diary_creation, day.day_name, entry.id AS entry_id, entry.exercise,
              entry.goal_reps, entry.goal_weight, entry.reps, entry.weight, entry.comments, entry.created_at entry_creation
          FROM diary
          LEFT JOIN day ON day.diary_id = diary.id
          LEFT JOIN entry ON entry.day_id = day.id
          WHERE owner = :user AND diary_id = :diary_id AND day_name = :day
          ORDER BY entry.id
          """), {"user": user, "diary_id": diary_id, "day": day}).fetchall()
      for row in explain2:
          print(row)
      if not entries:
        raise HTTPException(status_code=404, detail="This diary id and day name combination does not exist.")
      diary_entry = {"diary_id": diary_id, "created_at": entries[0].diary_creation, "day_name": day, "entries": []}
      for entry in entries:
        diary_entry["entries"].append({"entry_id": entry.entry_id, "created_at": entry.entry_creation, "exercise": entry.exercise,
            "goal_reps": entry.goal_reps, "goal_weight": entry.goal_weight, "reps": entry.reps, "weight": entry.weight, "comments": entry.comments})
      entry_list.append(diary_entry)
    return entry_list

@router.get("/plan/{diary_id}/{day}")
def get_plan(diary_id: int, day: str, user=Depends(user.get_user)):
  """Get the corresponding exercises and latest goal entries for a specific day in a specific diary."""
  entry_list = []
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).scalar_one()
      explain = connection.execute(sqlalchemy.text("EXPLAIN ANALYZE SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).fetchall()
      for row in explain:
        print(row)
    except NoResultFound:
      raise HTTPException(status_code=404, detail="A diary with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You do not own this diary.")
    entries = connection.execute(sqlalchemy.text("""
        WITH rankedEntry AS (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY day_id, exercise ORDER BY created_at DESC) ranking
          FROM entry
        )
        SELECT diary.id AS diary_id, diary.created_at diary_creation, day.day_name, entry.id AS entry_id, entry.exercise, entry.goal_reps,
            entry.goal_weight, entry.reps, entry.weight, entry.comments, entry.created_at entry_creation
        FROM diary
        LEFT JOIN day ON day.diary_id = diary.id
        LEFT JOIN rankedEntry entry ON entry.day_id = day.id AND entry.ranking = 1
        WHERE owner = :user AND diary_id = :diary_id AND day_name = :day
        """), {"user": user, "diary_id": diary_id, "day": day}).fetchall()
    explain2 = connection.execute(sqlalchemy.text("""
        DROP INDEX idx_day_diary_day_id, idx_entry_ranking;
        CREATE INDEX idx_day_diary_day_id ON day (diary_id, day_name);
        CREATE INDEX idx_entry_ranking ON entry (day_id, exercise, created_at DESC);
        EXPLAIN ANALYZE
        WITH rankedEntry AS (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY day_id, exercise ORDER BY created_at DESC) ranking
          FROM entry
        )
        SELECT diary.id AS diary_id, diary.created_at diary_creation, day.day_name, entry.id AS entry_id, entry.exercise, entry.goal_reps,
            entry.goal_weight, entry.reps, entry.weight, entry.comments, entry.created_at entry_creation
        FROM diary
        LEFT JOIN day ON day.diary_id = diary.id
        LEFT JOIN rankedEntry entry ON entry.day_id = day.id AND entry.ranking = 1
        WHERE owner = :user AND diary_id = :diary_id AND day_name = :day
        """), {"user": user, "diary_id": diary_id, "day": day}).fetchall()
    for row in explain2:
        print(row)
    if not entries:
      raise HTTPException(status_code=404, detail="This diary id and day name combination does not exist.")
    diary_entry = {"diary_id": diary_id, "created_at": entries[0].diary_creation, "day_name": day, "entries": []}
    for entry in entries:
      diary_entry["entries"].append({"entry_id": entry.entry_id, "created_at": entry.entry_creation,
          "exercise": entry.exercise, "goal_reps": entry.goal_reps, "goal_weight": entry.goal_weight})
    entry_list.append(diary_entry)
  return entry_list


@router.get("/previous/{diary_id}/{day}")
def get_previous(diary_id: int, day: str, user=Depends(user.get_user)):
  """Get the corresponding exercises and latest filled entries for a specific day in a specific diary."""
  entry_list = []
  with db.engine.begin() as connection:
    try:
      owner = connection.execute(sqlalchemy.text("SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).scalar_one()
      explain = connection.execute(sqlalchemy.text("EXPLAIN ANALYZE SELECT owner FROM diary WHERE id = :diary_id"), {"diary_id": diary_id}).fetchall()
      for row in explain:
        print(row)
    except NoResultFound:
      raise HTTPException(status_code=404, detail="A diary with this id does not exist.")
    if owner != user:
      raise HTTPException(status_code=401, detail="You do not own this diary.")
    entries = connection.execute(sqlalchemy.text("""
        WITH rankedEntry AS (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY day_id, exercise ORDER BY created_at DESC) ranking
          FROM entry
          WHERE reps IS NOT NULL AND weight IS NOT NULL
        )
        SELECT diary.id AS diary_id, diary.created_at diary_creation, day.day_name, entry.id AS entry_id, entry.exercise, entry.goal_reps,
            entry.goal_weight, entry.reps, entry.weight, entry.comments, entry.created_at entry_creation
        FROM diary
        LEFT JOIN day ON day.diary_id = diary.id
        LEFT JOIN rankedEntry entry ON entry.day_id = day.id AND entry.ranking = 1
        WHERE owner = :user AND diary_id = :diary_id AND day_name = :day
        """), {"user": user, "diary_id": diary_id, "day": day}).fetchall()
    explain2 = connection.execute(sqlalchemy.text("""
        DROP INDEX idx_day_diary_day_id, idx_entry_ranking;
        CREATE INDEX idx_day_diary_day_id ON day (diary_id, day_name);
        CREATE INDEX idx_entry_ranking ON entry (day_id, exercise, created_at DESC) WHERE reps IS NOT NULL AND weight IS NOT NULL;
        EXPLAIN ANALYZE
        WITH rankedEntry AS (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY day_id, exercise ORDER BY created_at DESC) ranking
          FROM entry
          WHERE reps IS NOT NULL AND weight IS NOT NULL
        )
        SELECT diary.id AS diary_id, diary.created_at diary_creation, day.day_name, entry.id AS entry_id, entry.exercise, entry.goal_reps,
            entry.goal_weight, entry.reps, entry.weight, entry.comments, entry.created_at entry_creation
        FROM diary
        LEFT JOIN day ON day.diary_id = diary.id
        LEFT JOIN rankedEntry entry ON entry.day_id = day.id AND entry.ranking = 1
        WHERE owner = :user AND diary_id = :diary_id AND day_name = :day
        """), {"user": user, "diary_id": diary_id, "day": day}).fetchall()
    for row in explain2:
        print(row)
    if not entries:
      raise HTTPException(status_code=404, detail="This diary id and day name combination does not exist.")
    diary_entry = {"diary_id": diary_id, "created_at": entries[0].diary_creation, "day_name": day, "entries": []}
    for entry in entries:
      diary_entry["entries"].append({"entry_id": entry.entry_id, "created_at": entry.entry_creation,
          "exercise": entry.exercise, "goal_reps": entry.goal_reps, "goal_weight": entry.goal_weight,
          "reps": entry.reps, "weight": entry.weight, "comments": entry.comments})
    entry_list.append(diary_entry)
  return entry_list