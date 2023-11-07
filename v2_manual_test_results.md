# Example workflow
## 2. Diary Deletion
Alvin is no longer going to the gym and wants to get rid of his exercise diary. Alvin takes steroids now so he does not need to go to the gym. Alvin knows that his diary_id is 11.

Alvin starts the process of deleting diary.

Starts by calling DELETE /diary/{diary_id} with diary_id as 11.
Then it returns success since that is his diary_id

## Testing results

* curl -X 'DELETE' \
  'https://exercisediary.onrender.com/diary/11' \
  -H 'accept: application/json'

* Response: 200
* Body: "OK" 


## 3. Getting a Past Entry and Inputting a New One
Jimmy is a daily gym goer and regular user of our exercise diary. Jimmy wants to get stronger and always tries to increase the hits max reps/weight from the last time he did the exercise. But Jimmy has Alzheimer's and can’t remember what his max reps/weight were for his squats from yesterday. Jimmy requests his diary with Get /diary/{diary_id}/{day} to get his exercises from the previous day (today is Wednesday, so Jimmy puts in {diary_id}, "Tuesday"). Jimmy will see a list of all his exercises from Tuesday. Next, Jimmy requests information for the squats exercise with Get /diary/{diary_id}/{day}/{exercise}. Jimmy will see the number of sets, weight, etc that is associated with his squats exercise. Finally, Jimmy will input his new squat stats for today by calling PATCH /diary/{diary_id}/{day}/{exercise} with his stats from today’s squats.

Jimmy wants to access the reps/weight for his squats in his diary and record his stats for today’s workout. To do so he:

First Jimmy calls /diary/{diary_id}/{day} with day=Tuesday to get his exercises from the previous day.
Next he calls /diary/{diary_id}/{day}/{exercise} with exercise=squats to access the stats for his squats from Tuesday.
Finally, Jimmy calls PATCH /diary/{diary_id}/{day}/{exercise} (day=Wednesday) to update his diary with his stats for squats for today in case he forgets again tomorrow.
Jimmy sets a new pr for squats and is ready to break his pr again tomorrow, even if he forgets this new pr.

## Testing results (Needs Updating)

1. 
* curl -X 'GET' \
  'https://exercisediary.onrender.com/diary/13/Tuesday' \
  -H 'accept: application/json'
Response: 200
Body: [ "Squats" ]

2. 

3. 
