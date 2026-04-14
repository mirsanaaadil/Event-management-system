Event Registration System

A simple web-based Event Registration System built using Python Flask and SQLite.  
This system allows users to view events, register for them, and lets admin manage events and view registrations.

--------------------------------------------------

Features

User:
- View available events
- Register for events
- View registered events (My Events)
- Logout

Admin:
- Add new events
- View all events
- View registered users
- Logout

--------------------------------------------------

Technologies Used

- Python (Flask)
- SQLite Database
- HTML, CSS
- Jinja2 Templates

--------------------------------------------------

Project Structure

Event-registration-system/

app.py  
database.db  

routes/  
    auth.py  
    admin.py  
    user.py  

templates/  
    login.html  
    admin_dashboard.html  
    add_event.html  
    view_registrations.html  
    user_dashboard.html  
    my_events.html  

static/  
    admin.css  
    user.css  
    login.css
    my_events.css
    view_registrations.css

README.md  

--------------------------------------------------

Installation and Setup

1. Create Folder named Event-registration-system

2. Navigate to project folder:
cd Event-registration-system

3. Create virtual environment:
python -m venv env

4. Activate environment:
env\Scripts\activate

5. Install Flask:
pip install flask

6. Create all files in their respective folders according to the project structure mentioned above. Ensure that HTML files are placed inside the templates folder, CSS files inside the static folder, and route files inside the routes folder.

6. Run the application:
python app.py

7. Open in browser:
http://127.0.0.1:5000/

8.

--------------------------------------------------

Git Workflow

1. Initialize Git (only first time)
git init
git add .
git commit -m "Initial project setup"

2. Connect to GitHub
git remote add origin <your-repocommit -link>
git branch -M main
git push -u origin main

3. Create Branches
git checkout -b frontend
git checkout -b backend

4. Work on a Feature
git checkout frontend

Make changes  then:

git add .
git commit -m "Added user dashboard UI"

5. Commit Frequently
After every small change:

git add .
git commit -m "Updated login page design"

Added login functionality
Fixed registration bug
Improved dashboard UI

6. Push to GitHub
git push origin frontend

7. Merge into Main

Step 1: Switch to main
git checkout main

Step 2: Pull latest
git pull origin main

Step 3: Merge branch
git merge frontend

Step 4: Push
git push origin main

8. Repeat for Backend
git checkout backend

git add .
git commit -m "Added event registration logic"
git push origin backend

Then merge same way.

Database

SQLite database (database.db)

Tables:
- users
- events
- registrations

--------------------------------------------------

Default Roles

Admin:
Can manage events and view registrations

User:
Can register and view events

--------------------------------------------------

Future Improvements

- Add event images
- Search and filter events
- Cancel registration option
- Email notifications
- Improve UI

--------------------------------------------------
