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
# LeCoVi imports
from app.database import AppModel, session


class TRestError(Exception):
    pass


class Student(AppModel):
    __tablename__ = 'students'

    description = None
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False, index=True)
    doc_type_id = Column(ForeignKey('document_types.id'))
    doc_number = Column(String(16), nullable=False, index=True)
    email = Column(String(256), nullable=False, index=True)

    doc_type = relationship('DocumentType')
    courses = relationship('Course', secondary='enrollments',
                           primaryjoin='and_('
                                       'Student.id==Enrollment.student_id)',
                           secondaryjoin='and_('
                                         'Enrollment.course_id==Course.id,'
                                         'Course.id>0,'
                                         'Course.erased==False)',
                           back_populates='students',
                           )

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

    @classmethod
    def get_or_create(cls, fields):
        """ Returns a Student object using `json_body` parameters.
        
        First we try to get a Student object using document number. If no 
        Student is registered in DB with the document number we try with 
        email address. If neither of both exists in DB, then we create a new 
        Student object.
        
        :param fields: a dictionary which contains Student data.
        """
        if not fields.get('doc_number') or not fields.get('email'):
            raise TRestError('missing doc_number or email field')

        student = cls.get_by(doc_number=fields.get('doc_number'))
        if not student:
            student = cls.get_by(doc_number=fields.get('email'))
            if not student:
                student = cls(
                    first_name=fields.get('first_name'),
                    last_name=fields.get('last_name'),
                    doc_type_id=fields.get('doc_type_id'),
                    doc_number=fields.get('doc_number'),
                    email=fields.get('email'),
                )
                session.commit()
        return student


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

    students = relationship('Student',
                            secondary='enrollments',
                            primaryjoin='and_('
                                        'Course.id==Enrollment.course_id)',
                            secondaryjoin='and_('
                                          'Enrollment.student_id==Student.id,'
                                          'Student.id>0,'
                                          'Student.erased==False)',
                            back_populates='courses',
                            )

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


class Enrollment(AppModel):
    __tablename__ = 'enrollments'

    description = None
    student_id = Column(ForeignKey('students.id'))
    course_id = Column(ForeignKey('courses.id'))
