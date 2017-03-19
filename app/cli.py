"""Usage:
    manage.py db migrate COMMENT
    manage.py db upgrade
    manage.py db drop
    manage.py db create [-d]
    manage.py db rebuild [-d]
    manage.py db history

Database operations.

Arguments:
  COMMENT  Database migration description.

Options:
  -h --help
  -d --demo-data  Populates DB with Demo Data.
"""
# Standard lib imports
import os
# Third-party imports
from alembic import command
from alembic.config import Config
from docopt import docopt
# BITSON imports
from app.database import session
from app.models import Student, DocumentType, Course
from config import BASEDIR


def drop_tables():
    Student.metadata.drop_all()
    from sqlalchemy.exc import ProgrammingError
    from .logger import console_logger

    try:
        session.execute('DROP TABLE "alembic_version";')
        session.commit()
    except ProgrammingError as error:
        console_logger.critical(error)


def create_all():
    Student.metadata.create_all()


def demo_data():
    document_types = [
        DocumentType(id=0, description='N/A'),
        DocumentType(description='DNI'),
        DocumentType(description='Passport'),
    ]
    session.add_all(document_types)

    courses = [
        Course(id=0, description='N/A', code='N/A', year=0, semester=0),
        Course(description='Arquitectura de computadoras',
               code='ARQ', year=1, semester=1),
        Course(description='Diagramación Lógica',
               code='DLO', year=1, semester=1),
        Course(description='Estructura de Datos',
               code='EDD', year=1, semester=2),
        Course(description='Paradigmas de Programación',
               code='PAR', year=1, semester=2),
        Course(description='Análisis de Sistemas',
               code='ASI', year=2, semester=1),
    ]
    session.add_all(courses)

    session.commit()

    students = [
        Student(id=0, first_name='N/A', last_name='N/A',
                doc_type=document_types[0],
                doc_number='0', email='none@mail.com', ),
        Student(first_name='Leandro E.', last_name='Colombo Viña',
                doc_type=document_types[1],
                doc_number='29076668', email='colomboleandro@ifts18.edu.ar',),
        Student(first_name='José', last_name='López',
                doc_type=document_types[1],
                doc_number='23546512', email='lopez@mail.com.ar',)
    ]
    session.add_all(students)
    session.commit()


def commands():
    arguments = docopt(__doc__)

    alembic_config_path = os.path.join(BASEDIR, 'alembic.ini')
    alembic_config = Config(alembic_config_path)

    if arguments['db']:
        if arguments['migrate']:
            command.revision(config=alembic_config,
                             message=arguments['COMMENT'],
                             autogenerate=True,
                             )

        if arguments['drop'] or arguments['rebuild']:
            drop_tables()

        if arguments['upgrade'] or arguments['create'] or arguments['rebuild']:
            command.upgrade(config=alembic_config, revision='head')

            if arguments['--demo-data']:
                demo_data()

        if arguments['history']:
            command.history(config=alembic_config, )

