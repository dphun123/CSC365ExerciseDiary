# Example workflow
## 2. Diary Deletion
Alvin is no longer going to the gym and wants to get rid of his exercise diary. Alvin takes steroids now so he does not need to go to the gym. Alvin knows that his diary_id is 1098 and his user_id is alvin.

Alvin starts the process of deleting diary.

Starts by calling DELETE /{diary_id}/{user_id} with diary_id is 1098 and user_id is alvin.
Then it returns success since that is his user_id and diary_id

## Testing results (Needs Updating)

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


## 3. Getting a Past Entry and Inputting a New One
Jimmy is a daily gym goer and regular user of our exercise diary. Jimmy wants to get stronger and always tries to increase the hits max reps/weight from the last time he did the exercise. But Jimmy has Alzheimer's and can’t remember what his max reps/weight were for his squats from yesterday. First, Jimmy requests his diary with Get /diary/{diary_id}. Then, Jimmy will call Get /diary/{diary_id}/{day} to get his exercises from the previous day (today is Wednesday). Jimmy will see a list of all his exercises from Tuesday. Next, Jimmy requests information for the squats exercise with Get /diary/{diary_id}/{day}/{exercise}. Jimmy will see the number of sets, weight, etc that is associated with his squats exercise. Finally, Jimmy will input his new squat stats for today by calling PATCH /diary/{diary_id}/{day}/{exercise} with his stats from today’s squats.

Jimmy wants to access the reps/weight for his squats in his diary and record his stats for today’s workout. To do so he:

starts by calling Get /diary/{diary_id} to access his diary.
then Jimmy calls /diary/{diary_id}/{day} with day=TUESDAY to get his exercises from the previous day.
next he calls /diary/{diary_id}/{day}/{exercise} with exercise=squats to access the stats for his squats from Tuesday.
finally, Jimmy calls PATCH /diary/{diary_id}/{day}/{exercise} to update his diary with his stats for squats for today in case he forgets again tomorrow.
Jimmy sets a new pr for squats and is ready to break his pr again tomorrow, even if he forgets this new pr.

## Testing results (Needs Updating)

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
  
