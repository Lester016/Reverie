# Reverie
A social network that enables the user's to print their friend's data.

![the-reverie herokuapp com_](https://user-images.githubusercontent.com/37885860/77821611-99211700-7126-11ea-893f-28e870cd34e5.png)

### Features:
1.) User's Authentication.

2.) Reset Password via Email.

3.) Post, View, Edit, Delete an Article.

4.) Share an Article.

5.) Add/Follow request on other users.

6.) Delete a Friend.

7.) Mutual Friends.

8.) Print the Friend's Data.

9.) User's Profile.

10.) Upload Image.

11.) Change Profile.

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
