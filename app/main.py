"""
    teachers-rest.main
    ~~~~~~~~~~~~~~~~~~~~~~

    Main module. This module creates falcon app.

    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
# Third-party imports
import falcon
# LeCoVi imports
from .models import Student, DocumentType, Course, session


def drop_tables():
    Student.metadata.drop_all()
    from sqlalchemy.exc import ProgrammingError
    from .logger import console_logger

    try:
        session.execute('DROP TABLE "alembic_version";')
        session.commit()
    except ProgrammingError as error:
        console_logger.critical(error)


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


api = falcon.API()
api.add_route('/students', Student())
api.add_route('/document_types', DocumentType())
api.add_route('/courses', Course())
