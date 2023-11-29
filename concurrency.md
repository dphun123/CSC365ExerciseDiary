# Concurency Control Mechanisms

## Issue 1
A Non Reapeatable Read could occur if a user (T1) accesses an exercise from a shared diary, then the owner of the diary (T2) changes the exercise to a different exercise. When T1 tries to access the same exercise, they will get a different result.
![IMG_0058](https://github.com/dphun123/ExerciseDiary/assets/77179475/c05ef329-facf-42ed-a3e4-672a8bcd9045)

## Issue 2
A Phantom Read could occur if a user (T1) request the exercises from a particular day from a shared diary, then the owner of the diary (T2) adds another exercise to the same day. When T1 requests the exercises from that day again, they will receive another excercise in addition to the ones they received previously. 
![IMG_0059](https://github.com/dphun123/ExerciseDiary/assets/77179475/a887789b-18a3-45a8-b78c-7bce8f119353)

## Issue 3
A Read Skew could occur if a user (T1) requests a shared diary, then the owner of the diary deletes that diary and creates a new diary with the same id. If T1 then requests the exersises from that diary id, T1 will have recieved the original diary, but the exercises from the new diary.
![IMG_0060](https://github.com/dphun123/ExerciseDiary/assets/77179475/afddd129-982e-48a0-a308-76c91933e0b0)

## Handling Concurency
The minimum isolation level required for our database would be serializable so that we can prevent phantom reads.
