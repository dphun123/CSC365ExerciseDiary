# Example Flows

## 1. Diary Creation with New Entry
Bob is a new user seeking to start tracking his exercises. He does not want to use a preset routine, but rather create his own. To do so, he must generate a new diary by calling POST /diary/, in which he submits his routine, let us say [Monday, Wednesday, Friday], for days. Then, with the diary_id, let us say 9001, he can add whatever exercises, let us say just bench press, he wants to a specific day, let us say on Monday, by calling POST/diary/{diary_id}/{day}, in which he submits Bench Press for Exercise and his goal weight and reps for goal_weight and goal_reps. With his diary set up, he can go to the gym and workout, after which he can add an entry to his diary. Let us say that Monday morning, he was able to bench press 225 pounds for 5 reps, then he would pass those values and any comments he has along with calling PATCH /diary/{entry_id}.

So, in order, he:
* starts by calling POST /diary/ and passing in [Monday, Wednesday, Friday] for days and NULL for copy_id to get a new diary with ID 9001.
* then Bob calls POST/diary/{diary_id}/{day} and passes in Bench Press for Exercise, his goal weight for goal_weight and his goal reps for goal_reps.
* while working out, he can record his progress by calling PATCH /diary/{entry_id} and passing in the numbers he was able to hit and since it was an easy workout, he enters "easy" as a comment.


## 2. Diary Deletion
Alvin is no longer going to the gym and wants to get rid of his exercise diary. Alvin takes steroids now so he does not need to go to the gym. Alvin knows that his diary_id is 1098 and his user_id is alvin. 

Alvin starts the process of deleting diary. 
* Starts by calling DELETE /diary_id / user_id with diary_id is 1098 and user_id is alvin.
* Then it returns success since that is his user_id and diary_id


## 3. Getting a Past Entry and Inputting a New One
Jimmy is a daily gym goer and regular user of our exercise diary. Jimmy wants to get stronger and always tries to increase the hits max reps/weight from the last time he did the exercise. But Jimmy has Alzheimer's and can’t remember what his max reps/weight were for his squats from yesterday. First, Jimmy requests his diary with Get /diary/{diary_id}. Then, Jimmy will call Get /diary/{diary_id}/{day}  to get his exercises from the previous day (today is Wednesday). Jimmy will see a list of all his exercises from Tuesday. Next, Jimmy requests information for the squats exercise with Get /diary/{diary_id}/{day}/{exercise}. Jimmy will see the number of sets, weight, etc that is associated with his squats exercise. Finally, Jimmy will input his new squat stats for today by calling PATCH /diary/{diary_id}/{day}/{exercise} with his stats from today’s squats. 

Jimmy wants to access the reps/weight for his squats in his diary and record his stats for today’s workout. To do so he:
* starts by calling Get /diary/{diary_id} to access his diary.
* then Jimmy calls /diary/{diary_id}/{day} with day=TUESDAY to get his exercises from the previous day.
* next he calls /diary/{diary_id}/{day}/{exercise} with exercise=squats to access the stats for his squats from Tuesday.
* finally, Jimmy calls PATCH /diary/{diary_id}/{day}/{exercise} to update his diary with his stats for squats for today in case he forgets again tomorrow.

Jimmy sets a new pr for squats and is ready to break his pr again tomorrow, even if he forgets this new pr.
