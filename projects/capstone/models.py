import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Date
from flask_migrate import Migrate

DB_PATH = os.environ['DATABASE_URI']
db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movie(db.Model):  
  __tablename__ = 'movies'
  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)

  def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

  def insert(self):
        db.session.add(self)
        db.session.commit()

  def update(self):
        db.session.commit()

  def delete(self):
        db.session.delete(self)
        db.session.commit()

  def __repr__(self):
        return f"<Movie id: '{self.id}' \nTitle: '{self.title}' \nRelease date: '{self.release_date}'>"


  def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release,
        }


class Actor(db.Model):
   __tablename__ = 'actors'

   id = Column(Integer, primary_key=True)
   name = Column(String)
   age = Column(String)
   gender = Column(String)

   def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

   def insert(self):
        db.session.add(self)
        db.session.commit()

   def update(self):
        db.session.commit()

   def delete(self):
        db.session.delete(self)
        db.session.commit()

   def __repr__(self):
        return f"<Actor id: '{self.id}' \nname: '{self.name}' \nAge: '{self.age}' \nGender: '{self.gender}'>"


   def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'release': self.age,
            'gender': self.gender
        }