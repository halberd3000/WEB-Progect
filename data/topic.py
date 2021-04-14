import sqlalchemy
import datetime
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Topic(SqlAlchemyBase):
    __tablename__ = 'topic'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    subcategory_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subcategory.id"))
    subcategory = orm.relation('Subcategory')
    user = orm.relation('User')
    message = orm.relation("Message", back_populates='topic')
