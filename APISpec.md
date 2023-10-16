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

### 2.1. Delete Diary - `/diary/{diary_id}/{user_id}` (DELETE)

**Returns**:

```json
{
    "success": "boolean"
}
```

## 3. Get Exercise and Recommendations
1. `Suggest Specific Type Excercise`

### 3.1 Suggest Specific Type Excercise - `/diary/{diary_id}{exercises}` (GET)

**Request**
```json
{
    "type": "string"
}
```


**Returns**:
```Json
{
    "exercises": "string[]",
    "weight": "int",
    "reps": "int"
}
```



## 4. Get Previous Exercise Entry
1. `Get Diary`
2. `Get Exercise`

### 4.1. Get Diary - `/diary/{diary_id}` (GET)

**Returns**:

```json
{
    "days": "int[]",
    "exercises": "string[]"
}
```

### 4.2. Get Exersise - `/diary/{diary_id}/{exersise}` (GET)

**Returns**:

```json
{
    "exercise": "string",
    "type": "string", /* as in the body part, later used for recommendations */
    "goal_weight": "int",
    "goal_reps": "int"
}
```
