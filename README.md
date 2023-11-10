# ExerciseDiary
## https://exercisediary.onrender.com/docs (no API key)
### aeji@calpoly.edu (Andrew Ji)
### ajung04@calpoly.edu (Alexander Jung)
### dphun@calpoly.edu (Dennis Phun)
### jcolt@calpoly.edu (Jack Colt)
We are planning on creating an exercise diary where users will be displayed either a week-by-week or set routine calendar. In this diary, they will be able to input exercises, sets, reps, comments, etc. that will be saved. Some features we are planning to implement include  possible exercise substitutions, sharing of routines, automatic exercise adjustment to ensure progression, and possibly some payment with user authentication (?). Furthermore, we plan to get info/descriptions for the exercises by scraping a website that has many.

## User Stories:
* As a heavy lifter, I want to keep track of my personal record for weight lifted by adding a comment on each exercise to have all of my records in one place.
* As a new gym person without a lot of time I would like to constantly change my routine in order to figure out which is the best and time efficient for my ever changing schedule.
* As the gym, I would like to keep track of exercises that trainers would suggest to new gym members so we can figure out what equipment we would need to buy more or which is being utilized the least.
* As a new lifter, I do not know what routine I am going to follow or even any exercises that I can do, so I want to be able to get a pre-set routine such that I will not have to think of anything other than what I have to do to get stronger.
* As an avid lifter, I want to be able to receive exercise substitutions for one of the exercises that are getting a bit stale, so that I can continue to enjoy going to the gym and progress in areas I am lacking.
* As a coach, I want to be able to share my pre-set routines, so that my clients will be able to receive them and follow along.
* As an average gym goer, I want to check my previous weight and reps for each exercise, so that I have an idea of what weight I should use currently.
* As a gym avoider, I want to log my hours spent at the gym, so that I can keep myself honest and lose the beer belly.
* As a gym rat, I want to create and save exercise routines, so that I can customize the length and intensity of my workouts in advance.
* As an athlete, I want to see exercises other athletes in my field are working on so I can match my competition or follow the most efficient plans.
* As an avid gym member, I want to see recommendations for exercises based on others who enjoy similar exercises to me.
* As someone who was recently injured, I want to see workout plans focused on PT for people who have had the same or a similar injury.

## Exceptions:
* Exception: missing input in the amount of reps
  - If the user does not enter an amount of rep then it will not be possible to add the exercise.
* Exception: duplicate exercises in same diary
  - If a user has the creates the same exercise then the user will get to choose to keep both or delete one.
* Exception: User has inputted the highest exercise so there is no possible recommendation
  - If the highest exercise for legs is squats and a user puts squats in their routine then the database has nothing to recommend as a higher or harder exercise.
* Exception: invalid input (e.g. letters) for # of sets
  - If a user's input is invalid for their # of sets, they will be asked to input a number. Also, we plan on having a dropdown menu as well.
* Exception: the user has put in their own exercise, but can't find any recommendations
  - If a user has created their own exercise, they will not be able to directly get recommendations. However, they may be able to put what body type the exercise is for (e.g. chest) and get recommendations then.
* Exception: attempted to share with a non-user
  - If a user is attempting to share with another user with an invalid username, they will be notified that the user does not exist and prompted for another.
* Exception: user has no previous entries for an exercise
  - If the user attempts to get their previous stats for an exercise, but has no previous entries, the user must be prompted that this is a new exercise.
* Exception: user logs more than 24 hours for a day
  - Workout hours would be entered for each day with the number of hours spent for that day, so if a user enters more than the number of hours possible in a day, we will keep them somewhat honest and prompt them to input again. 
* Exception: invalid time input
  - Exercises like the treadmill would ask for a time input. If users enters an invalid amount of time (e.g. 61 for seconds or minutes) they would be prompted to input the amount of time again.
* Exception: a user-made exercise conflicts with an existing exercise
  - Request that the user alter the name of their exercise +/ exercise description or overwrite theirs with the preset (assuming they’re the same)
* Exception: payment option gets declined
  - Inform user of error receiving payment and request alternate payment option
* Exception: user attempts to make a new account with an already registered email/username
  - Inform user that account already exists with given login info and swap from signup page to login page





 

