# Peer Review Reponse

## Code Comment Reviews

In add diary entry, there's 3 calls to the database. But we could combine these into one call and speed up the time for this API call. - fixed

Having authentication so I can't just do "my diary id - 1" to find someone else's diary would probably be a good idea. - fixed

Consider not having an API key required, as potential users should be able to access all the routes. 
- We would have in API key but feel like it is less steps to test and not too important since it is only a school project.

Consider adding return data validation so that FastAPI validates your return values.

Consider a ledger based design, so instead of UPDATE to change an entry, we can specify the new contents and in the event a user accidentally overwrote important data, customer service can roll it back easily.

Consider adding integration tests to test your code + db config before it goes into production.

Consider changing the FastAPI Title, desc, author to reflect the current project. As well as the root route message. - fixed

Add human readable errors if (For ex. ) an invalid diary id was entered. - fixed

Try to find a way, if possible, to avoid having the connection.execute() inside a for loop, this will be pretty slow because it has to send
and wait for quite a few queries. - fixed

Consider changing your create diary route to be /diary/create instead of /diary to clarify what the route is supposed to be. As
your other routes also start the route with /diary, it seems more like a category then an endpoint.  
- not done

Consider changing your HTTP verb for editing an entry to use PUT, which is more specific to Update operations. 
- changed to patch instead of PUT

Consider changing .first().id in the create diary route to .scalar_one(), which is more specific that you only want one
row with a single scalar. - fixed



In the add_entry function, consider using .scalar_one() to fetch the ids in the returned row, so that it raises an error if there are multiple rows returned with those unique conditions. - fixed

Consider handling errors more. For example if any of the queries that SELECT return none, be sure to check for that and proceed accordingly. - fixed with error messaged

Add logging in the functions to help with debugging.

Consider modifying the endpoint paths to be more descriptive in terms of what that specific endpoint does. For example, the delete endpoint is /diary/{diary_id}, so consider modifying it to something like /diary/delete/{diary_id}

Add docstrings to endpoints that need further explanation on what it does for more documentation.

In the add_entry function, add input validation to confirm that the diary to add the entry to already exists, and handle that case.

Consider implementing unit tests to ensure every endpoint is working as expected.

There’s some inconsistencies with the naming of classes and their respective functions. Class CreateEntry is associated with the add_entry function.

Some inconsistencies with the naming of attributes within classes. Consider changing goal_weight to weight or vice versa in the CreateEntry and EditEntry classes to be more readable.

For the last two GET methods, return the values in JSON format as specified in your APISpec.md, rather than just the raw values.



edit_entry should not hard code ok

ok should not be hard coded in delete

create diary_id and adding days should be done separately because they 
are not related

could make the create_diary inserts into 1 for more efficiency

can combine add_entry sql call into 1

create entry should be renamed to goal entry

add_entry adds a goal entry and edit_entry edits that entry
   
edit_entry should not be changing the goal because isn't an entry and a goal two different things

better naming conventions ensuring separation between goal weight and user entry

add_entry gives internal error and not sure which part is failing

add error messages

specify dates instead of days for al data types

change update to inserts to ledgerize data

if taking in days, lower information so days are consistent and add a checker to make sure only the days of the week are added

## Schema/API Design 
