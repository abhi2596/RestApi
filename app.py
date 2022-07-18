from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class TodoNote(db.Model):
    __tablename__ = "TodoNote"
    todo_note = db.Column(db.String(64),primary_key=True)
    todos = db.relationship("Todos",backref="todo_note")

class Todos(db.Model):
    __tablename__ = "Todos"
    id = db.Column(db.Integer,primary_key=True)
    todo = db.Column(db.String(64))
    completed = db.Column(db.String(64))
    todonote = db.Column(db.String,db.ForeignKey("TodoNote.todo_note"))

class TodosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todos
        include_fk  = True

note_schema = TodosSchema()
notelist_schema = TodosSchema(many=True)

class TodoNoteSchema(ma.Schema):
    class Meta:
        fields = ("todo_note","todos")
    todos = ma.Nested(TodosSchema,many=True)

todo_schema = TodoNoteSchema()
todolist_schema = TodoNoteSchema(many=True)
    
class TodoNoteList(Resource):
    def get(self):
        todos = TodoNote.query.outerjoin(Todos).all()
        return todolist_schema.dump(todos)
    
    def post(self):
        new_todo = TodoNote(
            todo_note = request.json["todo_note"]
        )
        db.session.add(new_todo)
        db.session.commit()
        return todo_schema.dump(new_todo)

class Todo_Note(Resource):
    def get(self,todo_note):
        todo = TodoNote.query.get(todo_note)
        return todo_schema.dump(todo)
    
    def put(self,todo_note):
        todo = TodoNote.query.get(todo_note)
        todo.todo_note = request.json["todo_note"]
        return todo_schema.dump(todo)

    def delete(self,todo_note):
        todo = TodoNote.query.get(todo_note)
        db.session.delete(todo)
        db.session.commit()
        return todo_schema.dump(todo)


class TodosList(Resource):
    def get(self,todo_note):
        todos = (
            Todos.query
            .filter_by(todonote=todo_note)
            .all()
        )
        return notelist_schema.dump(todos)
    
    def post(self,todo_note):
        todo = Todos(
            todo = request.json["todo"],
            completed = request.json["completed"],
            todonote = todo_note
        )
        db.session.add(todo)
        db.session.commit()
        return note_schema.dump(todo)

class Todo(Resource):
    def get(self,todo_note,todo):
        todo = (
            Todos.query
            .filter(Todos.todo==todo)
            .filter(Todos.todonote==todo_note)
            .first()
        )
        return note_schema.dump(todo)
    
    def put(self,todo_note,todo):
        todo = (
            Todos.query
            .filter(Todos.todonote==todo_note)
            .filter(Todos.todo==todo)
            .first()
        )
        todo.completed = request.json["completed"]
        db.session.add(todo)
        db.session.commit()  
        return note_schema.dump(todo)
    
    def delete(self,todo_note,todo):
        todo = (
            Todos.query
            .filter(Todos.todonote==todo_note)
            .filter(Todos.todo==todo)
            .first()
        )
        db.session.delete(todo)
        db.session.commit()
        return note_schema.dump(todo)


api.add_resource(TodoNoteList,"/todo_note")
api.add_resource(Todo_Note,"/todo_note/<string:todo_note>")
api.add_resource(TodosList,"/todo_note/<string:todo_note>/todo")
api.add_resource(Todo,"/todo_note/<string:todo_note>/todo/<string:todo>")



    
 






