This app is a POC made for a technical test in Django and docker. <br/>
It's supposed to let you log in either as a Doctor or a Patient. While patient will only have a simple view which contains their informations and consultations, <br/>
Doctors can display every patient present in DB, add, delete or update them and do the same for their consultations <br/>

Requirements : <br/>
  -Docker-compose <br/>


In order to start this app you will need to run the docker container using : ```docker-compose up --build``` (first time only, then simply use ```docker-compose up```) at the root of the directory. <br/>
Then navigate to ```cd test_tech``` <br/>
-```python3 manage.py runserver 0.0.0.0:8000``` <br/>
-if you need to create fake patients and 1 doctor you can use ```python3 -m consult_app.generate_patients``` from the project root (where you can find manage.py) <br/>

-Users will be created with raw passwords and username equal to their first name, in order to authenticate with these users, you will need to modify manually the associated password in django admin : <br/>
  -localhost:8000/admin/  <br/>
  -click user <br/>
  -select your user <br/>
  -modify password <br/>

-Now you can use the application at : http://localhost:8000/consult_app/
