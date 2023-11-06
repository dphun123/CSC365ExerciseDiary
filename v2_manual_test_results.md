# Example workflow
## 1. Diary Creation with New Entry
Bob is a new user seeking to start tracking his exercises. He does not want to use a preset routine, but rather create his own. To do so, he must generate a new diary by calling POST /diary/, in which he submits his routine, let us say [Monday, Wednesday, Friday], for days. Then, with the diary_id, let us say 9001, he can add whatever exercises, let us say just bench press, he wants to a specific day, let us say on Monday, by calling POST/diary/{diary_id}/{day}, in which he submits Bench Press for Exercise and his goal weight and reps for goal_weight and goal_reps. With his diary set up, he can go to the gym and workout, after which he can add an entry to his diary. Let us say that Monday morning, he was able to bench press 225 pounds for 5 reps, then he would pass those values and any comments he has along with calling PATCH /diary/{entry_id}.

So, in order, he:
1. starts by calling POST /diary/ and passing in [Monday, Wednesday, Friday] for days and NULL for copy_id to get a new diary with ID 9001.
2. then Bob calls POST/diary/{diary_id}/{day} and passes in Bench Press for Exercise, his goal weight for goal_weight and his goal reps for goal_reps.
3. while working out, he can record his progress by calling PATCH /diary/{entry_id} and passing in the numbers he was able to hit and since it was an easy workout, he enters "easy" as a comment.

# Testing results

1. 
* curl -X 'POST' \
  'http://localhost:3000/diary/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  "Monday", "Wednesday", "Friday"
]'
* Response: 9001

2. 
* curl -X 'POST' \
  'http://localhost:3000/diary/9001/Monday' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "exercise_name": "Bench Press",
  "goal_reps": 5,
  "goal_weight": 225
}'
* Response: 1

3. curl -X 'POST' \
  'http://localhost:3000/diary/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "reps": 5,
  "weight": 225,
  "comments": "easy"
}'
* Response: "OK"
