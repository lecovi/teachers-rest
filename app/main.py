"""
    teachers-rest.main
    ~~~~~~~~~~~~~~~~~~~~~~

    Main module. This module creates falcon app.

    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
import json
# Third-party imports
import falcon
# LeCoVi imports
from .models import TestModel


class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': 'I\'ve always been more interested in the future than in '
                     'the past.',
            'author': 'Grace Hopper'
        }

        resp.body = json.dumps(quote)


api = falcon.API()
api.add_route('/quote', QuoteResource())
api.add_route('/test', TestModel())
