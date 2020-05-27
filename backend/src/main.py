# coding=utf-8

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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasdfsadf'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)

Base.metadata.create_all(engine)

def token_required(func):
  def wrapper(*args, **kwargs):
    token = None

    if 'x-access-tokens' in request.headers:
      token = request.headers['x-access-tokens']
      
    if not token:
      return jsonify({'message': 'a valid token is missing'})

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      session = Session()
      current_user = session.query(User).filter_by(public_id=data['public_id']).first()
      session.close()
    except:
      return jsonify({'message': 'token is invalid'})

    return func(current_user, *args, **kwargs)
  wrapper.__name__ = func.__name__
  return wrapper


@app.route('/users')
def get_users():
  session = Session()
  user_objects = session.query(User).all()

  schema = UserSchema(many=True)
  users = schema.dump(user_objects)
  session.close()

  return jsonify(users)

@app.route('/register', methods=['POST'])
def register_user():
  posted_data = request.get_json()

  try:
    posted_user = UserSchema(only=('username', 'password')).load(posted_data)
  except ValidationError as err:
    response = jsonify(err.messages)
    response.status_code = 400
    return response

  # hashed_password = generate_password_hash(posted_user['password'], method='sha256')
  hashed_password = bcrypt.generate_password_hash(posted_user['password'])

  user = User(
    public_id=str(uuid.uuid4()),
    username=posted_user['username'],
    password=hashed_password.decode('utf-8', 'ignore'),
    admin=False,
    created_by='HTTP post request'
  )

  # persist user
  session = Session()
  session.add(user)
  session.commit()

  # return created user
  new_user = UserSchema().dump(user)
  session.close()
  return jsonify(new_user), 201

@app.route('/login', methods=['GET', 'POST'])
def login_user():
  # posted_user = UserSchema(only=('username', 'password')).load(posted_data)

  auth = request.authorization

  if not auth or not auth.username or not auth.password:
    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

  session = Session()
  user = session.query(User).filter_by(username=auth.username).first()
  session.close()

  if bcrypt.check_password_hash(user.password, auth.password):
    token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')})

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route('/users', methods=['DELETE'])
def remove_user():
  # mount user object
  deleted_user_id = request.get_json().get('id')

  # persist user
  session = Session()
  user = session.query(User).get(deleted_user_id)
  session.delete(user)
  session.commit()

  session.close()
  return jsonify('Deletion Successful'), 200

@app.route('/games', methods=['GET'])
def get_games():
  # fetching from the database
  session = Session()
  game_objects = session.query(Game).all()

  # transforming into JSON-serializable objects
  schema = GameSchema(many=True)
  games = schema.dump(game_objects)

  # serializing as JSON
  session.close()
  return jsonify(games)

@app.route('/game', methods=['POST'])
@token_required
def add_game(current_user):
  posted_data = request.get_json()
  posted_game = GameSchema(only=('title', 'secret_word', 'passphrase')).load(posted_data)
  game = Game(**posted_game, user_id=current_user.id, created_by="HTTP post request")

  session = Session()
  session.add(game)
  session.commit()
  new_game = GameSchema().dump(game)
  session.close()
  return jsonify(new_game), 201
  
  # response = 'You have access!'
  # response.status_code = 400
  # return response

@app.route('/games', methods=['DELETE'])
@token_required
def remove_game():
  deleted_game_id = request.get_json().get('id')

  session = Session()
  game = session.query(User).get(deleted_game_id)
  session.delete(game)
  session.commit()
  session.close()

  return jsonify('Deletion Successful'), 200
