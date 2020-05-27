# coding=utf-8

from marshmallow import Schema, fields, validates, ValidationError
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime

from .entity import Session, Entity, Base


class User(Entity, Base):
  __tablename__ = 'user'

  public_id = Column(String(36))
  username = Column(String(50))
  password = Column(String(length=128))
  admin = Column(Boolean(), default=False)

  games = relationship('Game')

  date_created = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, public_id, username, password, admin, created_by):
    Entity.__init__(self, created_by)
    self.public_id = public_id
    self.username = username
    self.password = password
    self.admin = admin

class UserSchema(Schema):
  id = fields.Number()

  public_id = fields.UUID()
  username = fields.Str(required=True)
  password = fields.Str(required=True)
  admin = fields.Bool()

  # Validations
  @validates('username')
  def is_unique(self, value):
    session = Session()
    is_unique = session.query(User).filter(User.username == value).first() is None
    session.close()
    if not is_unique:
      raise ValidationError('Username is already taken!')

  created_at = fields.DateTime()
  updated_at = fields.DateTime()
  last_updated_by = fields.Str()
