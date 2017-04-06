"""
    teachers-rest.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
import time
# Third-party imports
from sqlalchemy.exc import OperationalError
# LeCoVi imports
from .logger import console_logger


def wait_db_connection(engine, timeout=0):
    connected_to_db = False
    while not connected_to_db:
        try:
            engine.connect()
            connected_to_db = True
            console_logger.debug('Connected to {}'.format(engine.url))
        except OperationalError as error:
            timeout += 2
            time.sleep(timeout)
            console_logger.critical(error)
            console_logger.critical('Retrying in %d seconds...' % timeout)
