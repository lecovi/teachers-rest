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
from app.models import Student


class EnrollStudent:
    def on_post(self, req, resp):
        """ Handles Students enrollments """
        json_body = json.loads(req.stream.read().decode())

        student = Student.get_or_create(fields=json_body)

        courses_to_enroll = list()
        if json_body.get('arq'):
            courses_to_enroll.append('ARQ')
        if json_body.get('dlo'):
            courses_to_enroll.append('DLO')
        if json_body.get('asi'):
            courses_to_enroll.append('ASI')
        if json_body.get('par'):
            courses_to_enroll.append('PAR')
        if json_body.get('edd'):
            courses_to_enroll.append('EDD')

        student.multiple_enroll(course_code_list=courses_to_enroll)

        response = {
            'student': {
                'name': '{} {}'.format(student.first_name, student.last_name),
                'id': student.id,
                'email': student.email,
                'doc_number': student.doc_number,
                'doc_type': student.doc_type.description,
            },
            'courses': courses_to_enroll,
        }

        resp.body = json.dumps(response)

    def on_put(self, req, resp):
        """ Handles Students enrollment modifications"""
        json_body = json.loads(req.stream.read().decode())

        student = Student.get_or_create(fields=json_body)

        courses_to_enroll = list()
        courses_to_disenroll = list()
        if json_body.get('arq'):
            courses_to_enroll.append('ARQ')
        else:
            courses_to_disenroll.append('ARQ')
        if json_body.get('dlo'):
            courses_to_enroll.append('DLO')
        else:
            courses_to_disenroll.append('DLO')
        if json_body.get('asi'):
            courses_to_enroll.append('ASI')
        else:
            courses_to_disenroll.append('ASI')
        if json_body.get('par'):
            courses_to_enroll.append('PAR')
        else:
            courses_to_disenroll.append('PAR')
        if json_body.get('edd'):
            courses_to_enroll.append('EDD')
        else:
            courses_to_disenroll.append('EDD')

        student.multiple_enroll(course_code_list=courses_to_enroll)
        student.multiple_disenroll(course_code_list=courses_to_disenroll)

        response = {
            'student': {
                'name': '{} {}'.format(student.first_name, student.last_name),
                'id': student.id,
                'email': student.email,
                'doc_number': student.doc_number,
                'doc_type': student.doc_type.description,
            },
            'enrolled_courses': courses_to_enroll,
            'disenrolled_courses': courses_to_disenroll,
        }

        resp.body = json.dumps(response)

    def on_delete(self, req, resp):
        """ Handles Students disenrollments """
        json_body = json.loads(req.stream.read().decode())

        student = Student.get_or_create(fields=json_body)

        courses_to_disenroll = list()
        if json_body.get('arq'):
            courses_to_disenroll.append('ARQ')
        if json_body.get('dlo'):
            courses_to_disenroll.append('DLO')
        if json_body.get('asi'):
            courses_to_disenroll.append('ASI')
        if json_body.get('par'):
            courses_to_disenroll.append('PAR')
        if json_body.get('edd'):
            courses_to_disenroll.append('EDD')

        student.multiple_disenroll(course_code_list=courses_to_disenroll)

        response = {
            'student': {
                'name': '{} {}'.format(student.first_name, student.last_name),
                'id': student.id,
                'email': student.email,
                'doc_number': student.doc_number,
                'doc_type': student.doc_type.description,
            },
            'courses': courses_to_disenroll,
        }

        resp.body = json.dumps(response)
