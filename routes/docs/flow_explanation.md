Event Registration System Flow

1. Login / Authentication

- Users open the login page.
- User enters username and password.
- System checks credentials in the USERS table.
If valid:
- Stores user_id and role in session.
Redirects:
- Admin → Admin Dashboard
- User → User Dashboard
If invalid:
- Shows error message “Wrong username or password”.

2. Admin Dashboard Flow

Admin can add events:
- Inputs: Name, Date, Location, Description.
- Event is stored in the EVENTS table.

Admin can view registered users:
- System fetches data from REGISTRATIONS table, joins with USERS and EVENTS tables.
- Displays Username + Event Name in a table.

Admin can logout:
- Clears session and redirects to login page.

3. User Dashboard Flow

- User sees a list of available events from EVENTS table.

For each event, user can register:
- On registration, system checks REGISTRATIONS table for duplicates.
- If not registered, inserts user_id + event_id.
- Shows flash message: "Registered successfully" or "Already registered".

User can view my events:
- Fetches events from REGISTRATIONS table joined with EVENTS table where user_id matches.
- Displays event details: Name, Date, Location.

User can logout:
- Clears session and redirects to login page.

4. Database Relationships

- USERS (1) → (many) REGISTRATIONS
- EVENTS (1) → (many) REGISTRATIONS
- REGISTRATIONS table connects users to events (many-to-many relationship).