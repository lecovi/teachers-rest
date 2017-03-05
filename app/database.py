"""
    teachers-rest.database
    ~~~~~~~~~~~~~~~~~~~~~~
    
    Main DATABASE models. This modules set `AppModel` to use as a Template
    for new models in application.
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
import os
from datetime import datetime, date, time, timedelta
# Third-party imports
from sqlalchemy import (create_engine, Column, Integer, String, DateTime,
                        Boolean, Sequence, event)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
# LeCoVi imports
from app.logger import console_logger
from config import config

configuration = config[os.getenv('FALCON_CONFIG') or 'default']
engine = create_engine(configuration.SQLALCHEMY_DATABASE_URI)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


class AppModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100), nullable=False, index=True)
    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_on = Column(DateTime, default=datetime.utcnow(), nullable=False)
    erased = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        items = dict((col, getattr(self, col))
                     for col in self.__table__.columns.keys())
        row = "{}<{}>".format(self.__class__.__name__, items)
        return row

    def __str__(self):
        return "{} --> {}.id={}".format(self.__class__,
                                        self.__class__.__tablename__, self.id)

    def export_data(self, exclude=None):
        """
            This will return a dict instance of model. It works with jsonify.
        :param exclude: attribute name to exclude in response.
        :return: a dict().
        """
        response = dict()
        for attr, value in self.__dict__.items():
            if attr.startswith('_'):
                continue
            if exclude and attr in exclude:
                continue
            if isinstance(value, (date, time, datetime)):
                value = value.isoformat()
            if isinstance(value, timedelta):
                value = value.total_seconds()
            response.update({attr: value})
        return response

    @staticmethod
    def idempotent_insert(item_list):
        for item in item_list:
            try:
                session.add(item)
                session.commit()
            except IntegrityError as e:
                console_logger.warn(
                    "\033[33mWARNING: {}Skipping...\n\033[0m".format(
                        e.orig.args[0])
                )
                session.rollback()
                continue

    def _set_attr_in_db(self, key, value, commit=True):
        setattr(self, key, value)
        if commit:
            session.commit()

    def set_erased(self, commit=True):
        self._set_attr_in_db(key='erased', value=True, commit=commit)

    def set_not_erased(self, commit=True):
        self._set_attr_in_db(key='erased', value=False, commit=commit)

    @classmethod
    def get_by(cls, erased=False, **kwargs):
        return session.query(cls).filter_by(erased=erased, **kwargs).first()

    @classmethod
    def create_fake(cls, **kwargs):
        item = cls(**kwargs)
        item.fake = True
        session.add(item)
        session.commit()
        return item

    @classmethod
    def remove_fake(cls, item):
        if item.fake:
            if item.id > 1:
                cls.set_sequence_value(value=item.id - 1)
            session.delete(item)
            session.commit()

    @classmethod
    def get_sequence_name(cls):
        return "".join([cls.__tablename__, '_id_seq'])

    @classmethod
    def set_sequence_value(cls, value):
        sequence_name = cls.get_sequence_name()
        query = "SELECT setval('{sequence_name}', {value})".format(
            sequence_name=sequence_name, value=value)
        session.execute(query)
        session.commit()

    @classmethod
    def get_max_id(cls, erased=False):
        return session.query(func.max(cls.id)).filter_by(
            erased=erased).first()[0]

    @classmethod
    def get_invalid_id(cls):
        return session.query(func.max(cls.id)).first()[0] + 1

    @classmethod
    def update_sequence(cls, new_sequence_value=1):
        sequence = Sequence("".join([cls.__tablename__, "_id_seq"]))
        current_sequence_value = session.execute(sequence)
        while current_sequence_value < new_sequence_value:
            current_sequence_value = session.execute(sequence)


@event.listens_for(AppModel, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated_on = datetime.utcnow()