"""
    teachers-rest.models
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by Cooperativa de Trabajo BITSON Ltda..
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
import json
# Third-party imports
# BITSON imports
from app.database import AppModel


class TestModel(AppModel):
    __tablename__ = 'tests'

    def on_get(self, req, resp):
        test = {
            'k1': 'value1',
        }

        resp.body = json.dumps(test)
