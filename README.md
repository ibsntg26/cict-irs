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
    - GET request with parameter id (ex. /student/1 ) returns an instance

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
    - GET request with parameter id (ex. /incident/1 ) returns an instance

- http://127.0.0.1:8000/api/incident/student/
    - GET request returns all incident of logged student
    - GET request with parameter id (ex. /incident/1 ) returns an instance
    - POST request creates new incidents
    - PATCH request for processing/closing incidents
    
- http://127.0.0.1:8000/api/incident/evaluator/
    - GET request returns all incident of logged evaluator
    - GET request with parameter id (ex. /incident/1 ) returns an instance
    - PATCH request for processing/closing incidents

- http://127.0.0.1:8000/api/followup/
    - GET request returns all followups
    - GET request with parameter id (ex. /followup/1 ) returns an instance
    - POST request creates new followup

- http://127.0.0.1:8000/api/notification/
    - GET request returns all notifications
    - GET request with parameter user (ex. /incident/?user=1) returns all notification of that user
    - GET request with parameter id (ex. /notification/1 ) returns an instance
---

#### **SIDENOTES:**
- To deactivate the server: Hit `CTRL + C`
- To deactivate the env: Run `env\Scripts\deactivate`