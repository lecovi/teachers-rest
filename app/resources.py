"""
    teachers-rest.resources
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
import json
# Third-party imports
# LeCoVi imports
from app.models import Student, Course, DocumentType
from app.database import session


class EnrollStudent:
    def on_post(self, req, resp):
        """ Handles Students enrollment """
        json_body = json.loads(req.stream.read().decode())

        doc_type = DocumentType.get_by(id=json_body.get('doc_type_id'))
        new_student = Student(
            first_name=json_body.get('first_name'),
            last_name=json_body.get('last_name'),
            doc_number=json_body.get('doc_number'),
            email=json_body.get('email')
        )
        new_student.doc_type = doc_type
        session.commit()

        if json_body.get('arq'):
            course = Course.get_by(code='ARQ')
            new_student.courses.append(course)

        if json_body.get('dlo'):
            course = Course.get_by(code='DLO')
            new_student.courses.append(course)

        if json_body.get('asi'):
            course = Course.get_by(code='ASI')
            new_student.courses.append(course)

        if json_body.get('par'):
            course = Course.get_by(code='PAR')
            new_student.courses.append(course)

        if json_body.get('edd'):
            course = Course.get_by(code='EDD')
            new_student.courses.append(course)

        session.commit()
