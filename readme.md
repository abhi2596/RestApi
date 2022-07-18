## Rest Api Using flask

#### The packages used to build this api are 
#### flask_restful
#### flask_sqlalchemy
#### flask_marshmallow 

All the requirements required for the system are in the .venv folder. The only requirement is 
have python in the system. We need to activate the virtual environment to do this we need to 
navigate to the path this folder is present and then in Unix use this command 
"source .venv/Scripts/activate"
in Windows use this command ".venv/Scripts/activate"

Database was build using flask_sqlalchemy. There are two databases one is todo_note and the other 
is todos table. There are connected with one to many relationship from todo_note to todos table.

documentation.yml contains the API paths and what they do.
