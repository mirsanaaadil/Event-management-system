Database Schema

USERS
---------------------------------------------------------------------------
Field Name    | Data Type | Constraints        | Description
---------------------------------------------------------------------------
id            | INTEGER   | PRIMARY KEY        | Unique user ID
username      | TEXT      | NOT NULL, UNIQUE  | Username of the user
password      | TEXT      | NOT NULL          | Password of the user
role          | TEXT      | NOT NULL          | Role of user (admin/user)
---------------------------------------------------------------------------

EVENTS
---------------------------------------------------------------------------
Field Name    | Data Type | Constraints        | Description
---------------------------------------------------------------------------
id            | INTEGER   | PRIMARY KEY        | Unique event ID
name          | TEXT      | NOT NULL          | Name of the event
date          | TEXT      | NOT NULL          | Date of the event
location      | TEXT      | NOT NULL          | Location of the event
description   | TEXT      | NULL              | Description of the event
---------------------------------------------------------------------------

REGISTRATIONS
---------------------------------------------------------------------------
Field Name    | Data Type | Constraints        | Description
---------------------------------------------------------------------------
id            | INTEGER   | PRIMARY KEY        | Unique registration ID
user_id       | INTEGER   | NOT NULL, FK       | References USERS(id)
event_id      | INTEGER   | NOT NULL, FK       | References EVENTS(id)
---------------------------------------------------------------------------

Relationship
One user can register for many events
One event can have many users
So, many-to-many relationship using registrations table