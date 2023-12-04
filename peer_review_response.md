# Peer Review Reponse

## Code Comment Reviews

### Issue #1

- In add diary entry, there's 3 calls to the database. But we could combine these into one call and speed up the time for this API call.

  - Fixed. It is done in 2 because we have to insert to both the diary and day table.

- Having authentication so I can't just do "my diary id - 1" to find someone else's diary would probably be a good idea.

  - Implemented. Set up authentication/authorization for all the diary endpoints.

- Consider not having an API key required, as potential users should be able to access all the routes.

  - Fixed. We removed the API key and set up the FastAPI authorization with the authentication through the signup/login endpoints we created.

- Consider adding return data validation so that FastAPI validates your return values.

  - Not sure. We changed the returns to be key-value pairs such as {"diary_id": 1} when the return values were unclear it that's what this means.

- Consider a ledger based design, so instead of UPDATE to change an entry, we can specify the new contents and in the event a user accidentally overwrote important data, customer service can roll it back easily.

  - Not implemented. We decided not to implement this because it seems like an added feature.

- Consider adding integration tests to test your code + db config before it goes into production.

  - Not implemented. We understand the purpose, but are not willing to dedicate the time.

- Consider changing the FastAPI Title, desc, author to reflect the current project. As well as the root route message.

  - Fixed.

- Add human readable errors if (For ex. ) an invalid diary id was entered.

  - Implemented. Every endpoint has readable errors.

- Try to find a way, if possible, to avoid having the connection.execute() inside a for loop, this will be pretty slow because it has to send and wait for quite a few queries.

  - Fixed.

- Consider changing your create diary route to be /diary/create instead of /diary to clarify what the route is supposed to be. As
  your other routes also start the route with /diary, it seems more like a category then an endpoint.

  - Not implemented. POST implies creation.

- Consider changing your HTTP verb for editing an entry to use PUT, which is more specific to Update operations.

  - Fixed. Changed to PATCH instead of PUT.

- Consider changing .first().id in the create diary route to .scalar_one(), which is more specific that you only want one
  row with a single scalar.
  - Fixed.

### Issue #6

- In the add_entry function, consider using .scalar_one() to fetch the ids in the returned row, so that it raises an error if there are multiple rows returned with those unique conditions.

  - Fixed.

- Consider handling errors more. For example if any of the queries that SELECT return none, be sure to check for that and proceed accordingly.

  - Fixed. Added error messages to all endpoints.

- Add logging in the functions to help with debugging.

  - Not sure.

- Consider modifying the endpoint paths to be more descriptive in terms of what that specific endpoint does. For example, the delete endpoint is /diary/{diary_id}, so consider modifying it to something like /diary/delete/{diary_id}

  - Not implemented. DELETE implies delete.

- Add docstrings to endpoints that need further explanation on what it does for more documentation.

  - Implemented.

- In the add_entry function, add input validation to confirm that the diary to add the entry to already exists, and handle that case.

  - Implemented. create_entry now creates a new entry with error checking.

- Consider implementing unit tests to ensure every endpoint is working as expected.

  - Not implemented. Again, we understand the purpose, but are not willing to dedicate the time.

- There’s some inconsistencies with the naming of classes and their respective functions. Class CreateEntry is associated with the add_entry function.

  - Fixed. CreateEntry used in create_entry and EditEntry used in edit_entry.

- Some inconsistencies with the naming of attributes within classes. Consider changing goal_weight to weight or vice versa in the CreateEntry and EditEntry classes to be more readable.

  - Fixed. Only goal values in CreateEntry and both goal and regular values in EditEntry.

- For the last two GET methods, return the values in JSON format as specified in your APISpec.md, rather than just the raw values.
  - Fixed.

# Issue #11

- edit_entry should not hard code ok

  - Fixed. It now returns the edited entry in JSON.

- ok should not be hard coded in delete

  - Fixed. It now returns "Diary/Entry (id=...) successfully deleted."

- create diary_id and adding days should be done separately because they are not related

  - Not sure. They are related. Each diary has corresponding days that make up its routine.

- could make the create_diary inserts into 1 for more efficiency

  - Not implemented. We need 2 because it's 2 tables, but we did take the insert into days out of a for loop.

- can combine add_entry sql call into 1

  - Not implemented. We left it separate for error checking.

- create entry should be renamed to goal entry

  - Fixed. We did it the other way around. Rather than renaming the function, we renamed the class to both be CreateEntry.

- add_entry adds a goal entry and edit_entry edits that entry

  - Fixed. edit_entry now allows edits to the goal entry and adding/editing an actual entry.

- edit_entry should not be changing the goal because isn't an entry and a goal two different things

  - Fixed. See above.

- better naming conventions ensuring separation between goal weight and user entry

  - Fixed.

- add_entry gives internal error and not sure which part is failing

  - Not sure, probably fixed.

- add error messages

  - Implemented.

- specify dates instead of days for al data types

  - Not sure. The days are user specified day names for their diary.

- change update to inserts to ledgerize data

  - Not implemented. We decided not to ledgerize, but that is a good idea.

- if taking in days, lower information so days are consistent and add a checker to make sure only the days of the week are added
  - Not implemented. We wanted to allow users to make their own routines in their diaries. For example: "Push", "Pull", "Legs" would be a valid routine and each one represents a day.

## Schema/API Design

### Issue #2

- Currently the goal_reps and goal_weight is stored alongside each Entry. But I think that a lot of people would like to set a goal and have that carry forward to all their entries, instead of entering a goal each time.

  - Implemented. create_entry uses most recent goal values. Has error checking for the first entry needing goal values.

- Expose an actual date, instead of just arbitrary strings, might help keep everything consistent. Since I might want to have a gym diary, but I have to include every date when creating the diary and I might not have a routine that can nicely fit. I might just want to know when exactly I did an exercise.

  - Implemented. Diaries and entries now have created_at.

- When creating a new diary, there's an option to have it be a copy of an existing diary. I think it makes sense to extract this into its own route (maybe /diary/copy), just so we do not need to always specify NULL for a new entry.

  - Not implemented. We decided to scrap the endpoint.

- Add usernames/emails + passwords to your design. Since your ER diagram shows users with just a Name and ID, but we can
  spoof users pretty easily by trying other IDs, so integrating a email + (hashed) password would help to keep the users'
  diary entries secure.

  - Implemented. We used supabase auth to save emails and passwords when users signup and FastAPI auth form and supabase to authenticate users. All diary and entry endpoints are authorized by logging in.

- The users table also seems to have not made it into the schema. It would be nice to keep track of which diaries belong to which users.

  - Not implemented. We keep users saved with supabase auth, which is separate from the tables.

- Get Exercise Recommendations only includes 1 weight and reps for all exercises. It would be nice to be able to recommend
  a weight and rep goal for each exercise.

  - Not implemented. We decided to only have an exercise search endpoint.

- Instead of looking at a specific date for the last exercise, it would be nice to just find the last time I did a specific exercise.

  - Implemented somewhat. get_previous allows users to find their most recent filled entry for an exercise on a specific day in a specific diary.

- Your design currently doesn't track how long a user spent on an exercise, which was documented in your Exceptions.

  - Not implemented. We scrapped that.

- Currently the diary does not record which user created it.

  - Fixed. Diaries are linked to users.

- Almost all columns in your schema are allowed to be null, which could be non-null for some. For Ex, the day_id for entry. We do need to know when a specific entry happened.

  - Fixed.

- Consider having each entry associated directly with a diary, as someone might not have a defined date for each time they go to a gym. (They didn't setup a date per Weekday when creating a diary).

  - Not implemented. It would mess up some endpoints.

- Consider adding another entity for body parts since some exercises will exercise the same body part, it would be nice to model this in the relationships between the entities. It will also help with normalization because then we don't have any repeated information.

  - Not sure.

- There are a few syntax issues with your schema.sql. There are semicolons on line 51 and after a few insert statements. The table definition order causes some errors due to foreign key references being undefined.

  - Fixed. The ordering of table creation is now correct.

- Consider adding a route so that a user may add their own custom exercises.
  - Not implemented. We wanted a foreign key relation.

### Issue #7

- Consider separating the DDL (creating the tables) with the DML (inserts) into different scripts for better readability.

  - Fixed. We now only have the insert for the exercise table, removing the different flows.

- Implement the users class that is specified in the ERD, and pass those credentials in as parameters to the entry entities to reflect which diary/entries belong to which user.

  - Implemented somewhat. We used supabase auth instead. Diaries are linked to users.

- Add additional attributes to the user class than what is in the ERD that would make them unique. For example emails, phone numbers, password, etc. with a unique constraint.

  - Implemented. Users are differentiated by email.

- Add a foreign key constraint of the diary_id to the users table if implemented so diaries can be associated with which user created them.

  - Not implemented. Used supabase auth.

- Try adding comments to the schema.sql to better document what each table represents.

  - Not sure. Can see what tables represent already?

- Many columns of the entry table seem to be nullable, but I think it makes more sense for weight and/or reps to have to have a value when adding an entry

  - Fixed somewhat. We wanted them to be nullable because we have entry creation and entry edits accessing the same row.

- Consider modifying the delete diary endpoint to not actually delete that diary from the DB, but maybe add another column that indicates deletion and set that to True when deleted. This way, there is available history for the user if they accidentally delete a diary or other cases.

  - Not implemented. Don't care about logging.

- Avoid using just null as default type, and explicitly have a default type.

  - Implemented somewhat. Again, we wanted some values to be nullable, and a value like 0 would be valid, so there is nothing to default to that makes sense.

- In the entries table, foreign keys are allowed to be null, but I think they should be modified to be: day_id BIGINT NOT NULL, exercise_id BIGINT NOT NULL,

  - Fixed.

- An idea that would be cool to implement are enum categories of exercise types like cardio, push, pull, etc.

  - Implemented. We used this multiple times for the exercise search endpoint.

- Modify the endpoints to ensure they are all returning in JSON format.
  - Fixed.

### Issue #10

- New diary does not actually take in three strings for user_id, days, and copy_id as specified in api doc

  - Not implemented. We decided to scrap copying.

- The string value that /diary takes in could be improved with a datestring instead of a string
  - Not implemented. We wanted users to be able to have custom days such as "Push", "Pull", and "Legs".
- Day table take in date_time instead of ::text
  - Not implemented. See above.
- Days of the week should have more info and the date should be logged instead because the day can be gotten from that information
  - Not sure.
- Edit entry still returns ok if entry may or may not exist
  - Fixed. Added error checking.
- Day string in GET /diary/{diary_id}/{day} should be of type datestring
- /diary/{diary_id}{exercises} (GET) does not exist

  - Not implemented. We scrapped that.

- Rename diary to user_id and link user_id with name. Don’t need many diaries for one user. Associate goals, weights, info in different tables with relation to a user_id
  - Implemented somewhat. Users can have multiple diaries and are linked by email.
- Change get exercise for a day to get most recent weights and possibly add most recent weights for exercises with respect to a exercise group
  - Implemented. get_previous gets the latest filled entry for each exercise for a specific day in a specific diary.
- Separate goal_weights and goal_reps from reps and weight. The goal should be put in separately so they can work towards it as they upload their reps and weight
  - Fixed.
- /diary/{diary_id}/{day}/{exercise} days should not be used to look up a goal. A goal should be associated with a user/diary_id and the goal can contain goal weight, exercise, and date to reach it by. If you need the day of
  - Not implemented. It makes sense if you are doing the same exercises on each day, but you can just make a 1 day routine then.
- Delete always returns ok even for things i’ve previously deleted or for negative ids that I don’t think would be in the table
  - Fixed
- No information should be updated and things should be ledgerized so users can see their history
  - Not implemented.
