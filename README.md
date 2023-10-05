# splitwise_

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Prerequisite](#Prerequisite)
- [Installation](#Installation)
- [Functionalities](#Functionalities)
- [Further_Steps](#Further_Steps)


## About <a name = "about"></a>

Assignment:  Project is built over Django Rest Framework and used Sqlite3 as a database. In the project, We have to Split the Expenses between 4 friends and there are scenario like we have to split amount Equally , Exactly and on Percent basis.


## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing.

### Prerequisite

What things do you need to install the software and how to install them?

```
Python
Django Rest Framework
```

### Installation

A step-by-step series of examples that tell you how to get a development environment running.

Install the requirements.txt file for dependencies. run the below command: 
```
create virtual env : virtualenv venv

activate the env : 
For macOS and Linux: source venv/bin/activate
For Windows:  venv/Scripts/activate

pip3 install -r requirements.txt
```
### Functionalities
I have created the users using django management command. Code is in split/management/command. 

Using Command:
```
python3 manage.py create_user
```
There is database present in the project with every functionalities.

### Further_Steps

Start the django,by running the below command in different terminal (ensure the env is activated and dependencies were installed).

```
python3 manage.py migrate
python3 manage.py runserver
```


I have given the collections for all api in the directory of the source code.
