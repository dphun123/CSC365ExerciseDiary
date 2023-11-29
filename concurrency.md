# Concurency Control Mechanisms

## 1
A Non Reapeatable Read could occur if a user (T1) accesses an exercise from a shared diary, then the owner of the diary (T2) changes the exercise to a different exercise. When T1 tries to access the same exercise, they will get a different result.

## 2
A Phantom Read could occur if a user (T1) request the exercises from a particular day from a shared diary, then the owner of the diary (T2) adds another exercise to the same day. When T1 requests the exercises from that day again, they will receive another excercise in addition to the ones they received previously. 

## 3
