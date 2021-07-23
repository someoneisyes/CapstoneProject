import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_migrate import Migrate

database_name = "capstone"
database_path = 'postgresql://{}:{}@{}/{}'.format('postgres','postgres','localhost:5432', database_name)

db = SQLAlchemy()

#setup

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

##  the below function can be use to reset and start with new tables

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Movies(db.Model):  
  __tablename__ = 'movies'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120), nullable=False)
  release_date = db.Column(db.DateTime)
  rating = db.Column(db.Float)

  actor = db.relationship('Actors', secondary='link')

  def __init__(self, title, release_date, rating):
    self.title = title
    self.release_date = release_date
    self.rating = rating

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
      'title': self.title,
      'release_date': self.release_date,
      'rating': self.rating
    }

class Actors(db.Model):  
  __tablename__ = 'actors'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  age = db.Column(db.Integer)

  movie = db.relationship('Movies', secondary='link')

  def __init__(self, name, age):
    self.name = name
    self.age = age

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
      'name': self.name,
      'age': self.age
    }
  
class Link(db.Model):
  __tablename__ = 'link'

  movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
  actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), primary_key=True)