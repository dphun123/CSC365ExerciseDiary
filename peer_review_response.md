# Peer Review Reponse

## Code Comment Reviews

### Issue #1

- In add diary entry, there's 3 calls to the database. But we could combine these into one call and speed up the time for this API call.

  - Fixed. It is done in 2 because we have to insert to both the diary and day table.

- Having authentication so I can't just do "my diary id - 1" to find someone else's diary would probably be a good idea.

  - Fixed. Set up authentication/authorization for all the diary endpoints.

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

  - Fixed. Every endpoint has readable errors.

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

  - Fixed.

- In the add_entry function, add input validation to confirm that the diary to add the entry to already exists, and handle that case.

  - Fixed. create_entry now creates a new entry with error checking.

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

  - Fixed.

- specify dates instead of days for al data types

  - Not sure. The days are user specified day names for their diary.

- change update to inserts to ledgerize data

  - Not implemented. We decided not to ledgerize, but that is a good idea.

- if taking in days, lower information so days are consistent and add a checker to make sure only the days of the week are added
  - Not implemented. We wanted to allow users to make their own routines in their diaries. For example: "Push", "Pull", "Legs" would be a valid routine and each one represents a day.

## Schema/API Design
