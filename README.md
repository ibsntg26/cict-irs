#### **ON FIRST RUN, MAKE SURE TO DO THE FOLLOWING:**
1. Create and setup the virtual environment within the project directory. Assuming that you are using Python 3.10, run the following commands in terminal:
    - `python -m venv env` - creates a virtual environment
    - `pip install -r requirements.txt` - installs all the necessary dependencies

---

#### **TO RUN THE PROJECT, DO AS FOLLOWS:**
1. On terminal, CD to the project directory. Then, activate the virtual environment.
    - `env\Scripts\Activate`
2. Run the server
    - `python manage.py runserver`
    - server is at 127.0.0.1:8000

---

#### **API ENDPOINTS:**
- http://127.0.0.1:8000/api/user/
    - GET request returns all user
    - GET request with parameter id (ex. /user/1 ) returns an instance
    - GET request with parameter id and suspend action (ex. /user/1/suspend ) archives user
    - DELETE request with parameter id (ex. /user/1 ) deletes user


- http://127.0.0.1:8000/api/student/
    - GET request returns all student
    - GET request with parameter id (ex. /student/2018123456 ) returns an instance
    - POST request creates new student

http://127.0.0.1:8000/api/evaluator/
    - GET request returns all evaluator
    - GET request with parameter id (ex. /evaluator/2018123456 ) returns an instance
    - POST request creates new evaluator

- http://127.0.0.1:8000/api/incident/all/
    - GET request returns all incident
    - GET request with parameter status (ex. /all?status=open ) filters incident by status
    - GET request with parameter id (ex. /incident/1 ) returns an instance

- http://127.0.0.1:8000/api/incident/student/
    - GET request returns all incident of logged student
    - GET request with parameter status (ex. /student?status=open ) filters incident by status
    - GET request with parameter id (ex. /incident/1 ) returns an instance
    - POST request creates new incidents
    - PATCH request for processing/closing incidents
    
- http://127.0.0.1:8000/api/incident/evaluator/
    - GET request returns all incident of logged evaluator
    - GET request with parameter status (ex. /evaluator?status=open ) filters incident by status
    - GET request with parameter id (ex. /incident/1 ) returns an instance
    - PATCH request for processing/closing incidents

- http://127.0.0.1:8000/api/followup/
    - GET request returns all followups
    - GET request with parameter id (ex. /followup/1 ) returns an instance
    - POST request with parameter res (ex. /followup/?res=1) creates new followup

- http://127.0.0.1:8000/api/notification/
    - GET request returns all notifications
    - GET request with parameter user (ex. /incident/?user=1) returns all notification of that user
    - GET request with parameter id (ex. /notification/1) returns an instance

- http://127.0.0.1:8000/api/event/
    - GET request returns all events
    - GET request with parameter id (ex. /event/1) returns an instance
    - DELETE request with parameter id (ex. /event/1) deletes an instance

- http://127.0.0.1:8000/api/news/
    - GET request returns all news
    - GET request with parameter id (ex. /news/1) returns an instance
    - DELETE request with parameter id (ex. /news/1) deletes an instance

---

#### **SIDENOTES:**
- To deactivate the server: Hit `CTRL + C`
- To deactivate the env: Run `env\Scripts\deactivate`