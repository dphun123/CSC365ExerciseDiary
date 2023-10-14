# API Specification

## 1. Diary Creation
1. `New Diary`
2. `Add Exercise`
3. `Add Entry`

### 1.1. New Diary - `/diary/` (POST)


Creates a new diary.


**Request**:


```json
{
  "user_id": "string", /* potentially used for authentication */
  "days": "[day1, day2, day3, ...]", /* can be any amount of days, custom-named, etc. */
  "copy_id": "string" /* existing diary_id to copy or NULL*/
}
```


**Returns**:


```json
{
    "diary_id": "string" /* used for future calls */
}
```

### 1.2.1 Add Exercise to Diary on a Specific Day - `/diary/{diary_id}/{day}/` (PUT)

Adds an exercise to a specific day in the diary. This would be included in all future entries.

**Request**:

```json
{
  "exercise": "string",
  "type": "string", /* as in the body part, later used for recommendations */
  "goal_weight": "int",
  "goal_reps": "int"
}
```

**Returns**:

```json
{
    "success": "boolean"
}
```

### 1.2.2 Remove Exercise from Diary on a Specific Day - `/diary/{diary_id}/{day}/{exercise}` (DELETE)

Removes an exercise from a specific day in the diary. This would be removed from all future entries.

**Request**:

```json
{

}
```

**Returns**:

```json
{
    "success": "boolean"
}
```

### 1.3. Edit Diary - `/diary/{diary_id}/{day}/{exercise}` (PATCH)

**Request**:

```json
{
    "weight": "int",
    "reps": "int",
    "comments": "string" /* optional */
}
```

**Returns**:

```json
{
    "success": "boolean"
}
```



## 2. Diary Deletion
1. `Delete Diary`

### 2.1. Delete Diary - `/diary/{diary_id}` (DELETE)



## 3. Get Exercise Recommendations



