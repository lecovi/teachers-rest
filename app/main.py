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

from .models import Student, DocumentType, Course

api = falcon.API()
api.add_route('/students', Student())
api.add_route('/document_types', DocumentType())
api.add_route('/courses', Course())
