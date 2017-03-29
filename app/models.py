"""
    teachers-rest.models
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Application DB Models.
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
import json
# Third-party imports
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# BITSON imports
from app.database import AppModel, session


class Student(AppModel):
    __tablename__ = 'students'

    description = None
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False, index=True)
    doc_type_id = Column(ForeignKey('document_types.id'))
    doc_number = Column(String(16), nullable=False, index=True)
    email = Column(String(256), nullable=False, index=True)

    doc_type = relationship('DocumentType')

    def on_get(self, req, resp):
        results = session.query(Student).filter(Student.id > 0,
                                                Student.erased == False).all()

        students = list()
        for result in results:
            student = {
                'id': result.id,
                'first_name': result.first_name,
                'last_name': result.last_name,
                'doc_type': result.doc_type.description,
                'doc_number': result.doc_number,
                'email': result.email,
                'created_on': result.created_on.isoformat(),
                'updated_on': result.updated_on.isoformat(),
            }
            students.append(student)

        response = {
            'objects': students,
            'results': len(students),
        }

        resp.body = json.dumps(response)


class DocumentType(AppModel):
    __tablename__ = 'document_types'

    def on_get(self, req, resp):
        results = session.query(DocumentType).filter(
            DocumentType.id > 0, DocumentType.erased == False).all()

        document_types = list()
        for result in results:
            document_type = {
                'id': result.id,
                'description': result.description,
                'created_on': result.created_on.isoformat(),
                'updated_on': result.updated_on.isoformat(),
            }
            document_types.append(document_type)

        response = {
            'objects': document_types,
            'results': len(document_types),
        }

        resp.body = json.dumps(response)


class Course(AppModel):
    __tablename__ = 'courses'

    year = Column(Integer, nullable=False, default=1)
    semester = Column(Integer, nullable=False, default=1)
    code = Column(String(3), nullable=False, index=True)

    def on_get(self, req, resp):
        results = session.query(Course).filter(
            Course.id > 0, Course.erased == False).all()

        courses = list()
        for result in results:
            course = {
                'id': result.id,
                'description': result.description,
                'code': result.code,
                'year': result.year,
                'semester': result.semester,
                'created_on': result.created_on.isoformat(),
                'updated_on': result.updated_on.isoformat(),
            }
            courses.append(course)

        response = {
            'objects': courses,
            'results': len(courses),
        }

        resp.body = json.dumps(response)

    def on_post(self, req, resp):
        json_body = json.loads(req.stream.read().decode())
        self.set_attr_from_dict(dictionary=json_body)
        print(json_body)
