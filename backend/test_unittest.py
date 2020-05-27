import os
import unittest

from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_bcrypt import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
from marshmallow import ValidationError
import uuid
import jwt

from .entities.entity import Session, engine, Base, db_uri
from .entities.user import User, UserSchema
from .entities.game import Game, GameSchema

class Test_TestBackend(unittest.TestCase):
  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'asdfasdfsadf'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    self.app = app.test_client()
    # db.create_all()
    db = SQLAlchemy(self.app)
    migrate = Migrate(self.app, db)

    bcrypt = Bcrypt(self.app)
    CORS(self.app)

    Base.metadata.create_all(engine)

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_user_registration(self):
    test_password = 'goldfish'
    test_password_hash = bcrypt.generate_password_hash(test_password).decode('utf-8', 'ignore')
    test_user = User(
      public_id='0c900d5e-d2e1-4edb-aaba-782529afc363',
      username='johndoe',
      password=test_password_hash,
      admin=False,
      created_by='HTTP post request'
    )

    assert bcrypt.check_password_hash(user.password, test_password)

  # def test_make_unique_nickname(self):
  #   u = User(nickname='john', email='john@example.com')
  #   db.session.add(u)
  #   db.session.commit()
  #   nickname = User.make_unique_nickname('john')
  #   assert nickname != 'john'
  #   u = User(nickname=nickname, email='susan@example.com')
  #   db.session.add(u)
  #   db.session.commit()
  #   nickname2 = User.make_unique_nickname('john')
  #   assert nickname2 != 'john'
  #   assert nickname2 != nickname


if __name__ == '__main__':
  unittest.main()
