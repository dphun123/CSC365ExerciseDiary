import sqlalchemy
import database as db
from faker import Faker

NUM_USERS = 5000
fake = Faker()

diary1_days = ["Upper", "Lower"]
diary2_days = ["Push", "Pull", "Legs"]
diary1_values = []
diary2_values = []
entries_to_insert = []

users = set()

while len(users) < NUM_USERS:
    users.add(fake.email())

with db.engine.begin() as connection:
    for user in users:
        diary_id_1 = connection.execute(sqlalchemy.text("INSERT INTO diary(owner) VALUES (:user) RETURNING id"), {"user": user}).scalar_one()
        diary1_values.extend({"day_name": day, "diary_id": diary_id_1} for day in diary1_days)
        diary_id_2 = connection.execute(sqlalchemy.text("INSERT INTO diary(owner) VALUES (:user) RETURNING id"), {"user": user}).scalar_one()
        diary2_values.extend({"day_name": day, "diary_id": diary_id_2} for day in diary2_days)
    connection.execute(sqlalchemy.text("INSERT INTO day (day_name, diary_id) VALUES (:day_name, :diary_id)"), diary1_values)
    connection.execute(sqlalchemy.text("INSERT INTO day (day_name, diary_id) VALUES (:day_name, :diary_id)"), diary2_values)

with db.engine.begin() as connection:
    for day_name in diary1_days + diary2_days:
        for user in users:
            day_id = connection.execute(sqlalchemy.text("""
                SELECT day.id
                FROM day
                JOIN diary ON day.diary_id = diary.id
                WHERE day_name = :day_name AND owner = :user
                LIMIT 1"""), {"day_name": day_name, "user": user}).scalar_one()
            entries_to_insert.extend(
                {"day_id": day_id, "exercise": "Barbell Squat", "goal_reps": 5, "goal_weight": 315,
                 "reps": 5, "weight": 315, "comments": "Good."} for _ in range(8))
            entries_to_insert.extend(
                {"day_id": day_id, "exercise": "Chest dip", "goal_reps": 5, "goal_weight": 90,
                 "reps": 5, "weight": 90, "comments": "Good."} for _ in range(8))
            entries_to_insert.extend(
                {"day_id": day_id, "exercise": "Dumbbell Bench Press", "goal_reps": 10, "goal_weight": 110,
                 "reps": 10, "weight": 110, "comments": "Good."} for _ in range(8))
            entries_to_insert.extend(
                {"day_id": day_id, "exercise": "Pullups", "goal_reps": 8, "goal_weight": 45,
                 "reps": 8, "weight": 45, "comments": "Good."} for _ in range(8))
            entries_to_insert.extend(
                {"day_id": day_id, "exercise": "Barbell Deadlift", "goal_reps": 5, "goal_weight": 405,
                 "reps": 5, "weight": 405, "comments": "Good."} for _ in range(8))
    connection.execute(sqlalchemy.text("""
        INSERT INTO entry (day_id, exercise, goal_reps, goal_weight, reps, weight, comments)
        VALUES (:day_id, :exercise, :goal_reps, :goal_weight, :reps, :weight, :comments)
        """), entries_to_insert)
