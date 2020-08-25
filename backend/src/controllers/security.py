import os
from flask import g, current_app as app
import jwt
from jwt.exceptions import DecodeError

JWT_ISSUER = 'com.jack.connexion'
JWT_SECRET = os.getenv('SECRET')
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'


def decode_token(token):
  # token = None
  # if 'x-access-tokens' in request.headers:
  #   token = request.headers['x-access-tokens']
  if not token:
    return jsonify({'error': ['a valid token is missing']}), 401
  try:
    data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    # session = Session()
    # current_user = g.session.query(User).filter_by(public_id=data['public_id']).first()
    # session.close()
    return data
  except DecodeError as e:
    print(f'decode failed {e}')
    return jsonify({'error': [e]})
