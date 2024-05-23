# webapps2024

This is a paypal clone for the third year module Web Applications and Services required for my BCS Degree from the University of Sussex.

Tech Stack:
Full native Django app with HTML templating.

Outcomes:
Django Templating and View intergration.
RESTful API service for currency exchange.
Database models for data persistance.
Real time notification system via websockets. 

How to run locally:

1.) Open a new terminal.

2.) Run command "pip install -r requirements.txt"

2.) Run command "python manage.py makemigrations".

3.) Run command "python manage.py migrate".

4.) Run command "daphne -e ssl:port=443:privateKey=localhost.key:certKey=localhost.crt webapps20
24.asgi:application" for HTTPS local server that also handles ASGI Websockets. 
(PEM pass phrase: "webapps") 

5.) Web app will be running at https://127.0.0.1:443/.

6.) Admin login: Username: 'admin1' | Password: 'admin1'

