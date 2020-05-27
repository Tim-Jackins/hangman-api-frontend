# coding=utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, ForeignKey#, backref
from sqlalchemy.orm import relationship

from .entity import Entity, Base


class Game(Entity, Base):
  __tablename__ = 'game'

  name = Column(String)
  secret_word = Column(String)
  password = Column(String)

  user_id = Column(Integer, ForeignKey('user.id'))

  def __init__(self, name, secret_word, passphrase, user_id):
    Entity.__init__(self, created_by)
    self.name = name
    self.secret_word = secret_word
    self.passphrase = passphrase
    self.user_id = user_id

    # self.user = user

class GameSchema(Schema):
  id = fields.Number()

  name = fields.Str()
  secret_word = fields.Str()
  passphrase = fields.Str()
  # user = fields.Int()
  description = fields.Str()

  created_at = fields.DateTime()
  updated_at = fields.DateTime()
  last_updated_by = fields.Str()
