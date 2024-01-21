This app is a POC made for a technical test in Django and docker.
It's supposed to let you log in either as a Doctor or a Patient. While patient will only have a simple view which contains their informations and consultations, 
Doctors can display every patient present in DB, add, delete or update them and do the same for their consultations

Requirements : 
  -Docker-compose


In order to start this app you will need to run the docker container using : ```docker-compose up --build``` at the root of the directory.
Then navigate to ```cd test_tech``` 
-```python3 manage.py runserver 0.0.0.0:8000```
-if you need to create fake patients and 1 doctor you can use ```python3 -m consult_app.generate_patients``` from the project root (where you can find manage.py

-Users will be created with raw passwords and username equald to their first name, in order to authenticate with these users, you will need to modify manually the associated password in django admin :
  -localhost:8000/admin/
  -click user
  -select your user
  -modify password

-Now you can use the application at : http://localhost:8000/consult_app/
