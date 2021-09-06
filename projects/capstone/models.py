import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , timedelta
import json

DB_PATH = os.environ['DATABASE_URI']
db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Table(db.Model):  
  __tablename__ = 'table'

  id = Column(Integer, primary_key=True)
  chairs_num = Column(Integer)
  reservation= db.relationship('Reservation', lazy=True)

  def __init__(self, chairs_num ):
    self.chairs_num = chairs_num

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'chairs_num': self.chairs_num,
    }


class Reservation(db.Model):  
  __tablename__ = 'reservation'

  id = Column(Integer, primary_key=True)
  account =Column(String , nullable=False )
  guest =Column(String , nullable=False )
  table_id = Column(Integer, db.ForeignKey('table.id', ondelete='CASCADE'), nullable=False)
  appointmentـTime = Column( db.DateTime , default=datetime.utcnow() + timedelta(days=1) ,nullable=False )

  def __init__(self, account , guest , table_id , appointmentـTime ):
    self.account = account
    self.guest = guest
    self.table_id = table_id
    self.appointmentـTime = appointmentـTime

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'account':self.account,
      'table_id': self.table_id,
      'guest': self.guest,
      'appointmentـTime':self.appointmentـTime
    }


class Menu(db.Model):  
  __tablename__ = 'menu'

  id = Column(Integer, primary_key=True)
  dish_name = Column(String)
  category = Column(String)
  description = Column(String)
  price = Column(String)   #make it integer

  def __init__(self, dish_name, description, category, price ):
    self.dish_name = dish_name
    self.description= description
    self.category = category
    self.price =  price

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'dish_name': self.dish_name,
      'description': self.description,
      'category': self.category,
      'price': self.price
    }

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    
    table = Table(chairs_num = 1)
    table.insert()

    table = Table(chairs_num = 2)
    table.insert()

    table = Table(chairs_num = 3)
    table.insert()

    table = Table(chairs_num = 4)
    table.insert()

    table = Table(chairs_num = 5)
    table.insert()

    table = Table(chairs_num = 6)
    table.insert()

    table = Table(chairs_num = 8)
    table.insert()


    reservation = Reservation(account='jalal@hotmail.com', guest='jalal',table_id= 1,appointmentـTime= "2021-10-07 00:45:12")
    reservation.insert()

    reservation = Reservation(account='ali@gmail.com', guest='ali',table_id= 2,appointmentـTime= "2021-03-12 00:55:31")
    reservation.insert()
    

    reservation = Reservation(account='ahmed@gmail.com', guest='ahmed',table_id= 3,appointmentـTime= "2021-11-34 00:18:27")
    reservation.insert()


    reservation = Reservation(account='mohmmed@gmail.com', guest='mohmmed',table_id= 3,appointmentـTime= "2021-06-22 00:22:14 ")
    reservation.insert()

    menu = Menu(dish_name = 'Big Mouth Burger',category = 'Burgers',description = "cheese, ketchup, mayonnaise",price = '15$')
    menu.insert()

    menu = Menu(dish_name = 'Beef Burger',category = 'Burgers',description = "ketchup, cheese, mayonnaise",price = '20$')
    menu.insert()

    menu = Menu(dish_name = 'Grilled Chicken Sandwich',category = 'Sandwiches',description = "ketchup",price = '23$')
    menu.insert()

    menu = Menu(dish_name = 'Seafood Sandwich',category = 'Sandwiches',description = "cheese",price = '16$')
    menu.insert()

    menu = Menu(dish_name = 'Cakes',category = 'Desserts',description = "Make the dough light",price = '12$')
    menu.insert()

    menu = Menu(dish_name = 'Confection',category = 'Desserts',description = "Make the dough light",price = '15$')
    menu.insert()

    menu = Menu(dish_name = 'Grape Juice',category = 'Juices',description = "little sugar",price = '10$')
    menu.insert()

    menu = Menu(dish_name = 'Carrot Juice',category = 'Juices',description = "More sugar",price = '17$')
    menu.insert()