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

        student = Student.get_or_create(fields=json_body)

        if json_body.get('arq'):
            course = Course.get_by(code='ARQ')
            student.courses.append(course)

        if json_body.get('dlo'):
            course = Course.get_by(code='DLO')
            student.courses.append(course)

        if json_body.get('asi'):
            course = Course.get_by(code='ASI')
            student.courses.append(course)

        if json_body.get('par'):
            course = Course.get_by(code='PAR')
            student.courses.append(course)

        if json_body.get('edd'):
            course = Course.get_by(code='EDD')
            student.courses.append(course)

        session.commit()
