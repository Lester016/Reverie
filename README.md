# Reverie
A blogging platform that enables the author to make a network and print their data.

### How to set up:

#### Windows
1.) Go to the project directory.

2.) Create a virtual environment 
`$ py -3 -m venv venv`

3.) Activate the virtual environment
`$ venv\Scripts\activate`

4.) Install the requirements.txt using this commad `$ pip install -r requirements.txt`

##### Type the following command to export the settings of our app configuration.

`$ set FLASK_APP=run.py`

`$ set FLASK_ENV=development`

`$ set SECRET_KEY='justarandomkey'`

`$ set SQLALCHEMY_DATABASE_URI=sqlite:///site.db`

You need to provide a valid email. The email will be used to send a mail for resetting the user password.

`$ set EMAIL_USER=YourEmailUser@gmail.com`

`$ set EMAIL_PASS=YourEmailPassword`

`$ flask run`



#### Linux
1.) Go to the project directory.

2.) Create a virtual environment 
`$ python3 -m venv venv`

3.) Activate the virtual environment
`$ . venv/bin/activate`

4.) Install the requirements.txt using this commad `$ pip install -r requirements.txt`

##### Type the following command to export the settings of our app configuration.

`$ export FLASK_APP=run.py`

`$ export FLASK_ENV=development`

`$ export SECRET_KEY='justarandomkey'`

`$ export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'`

You need to provide a valid email. The email will be used to send a mail for resetting the user password.

`$ export EMAIL_USER='YourEmailUser@gmail.com'`

`$ export EMAIL_PASS='YourEmailPassword'`

`$ flask run`
