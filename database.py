# -*- coding:utf-8 -*-
#--- SQLALCHEMY SUPPORT
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from extensions import db


db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db.engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import User
    Base.metadata.create_all(bind=db.engine)
    

def drop_all():
    db.drop_all()


def create_all():
    db.create_all()


def remove_session():
    db.session.remove()

#--- SQLALCHEMY SUPPORT END
