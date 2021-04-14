import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Subcategory(SqlAlchemyBase):
    __tablename__ = 'subcategory'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("category.id"))
    category = orm.relation('Category')
    topic = orm.relation("Topic", back_populates='subcategory')
