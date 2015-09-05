# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 21:40:35 2015

@author: Robert Smith
"""

from db_utils.base import ABC_Database

import os
import pyodbc

import logging

logger = logging.getLogger(__name__)


class SQLite(ABC_Database):
    """\
    MS Access Database interaction object

    Members:
        driver string text for system installed driver
        dbq string full file path to access database

    Methods:
        db_execute executes SQL against stored database
        create_accdb creates new MS Access db and returns new Access object pointing to the database
    """
    _connect = None
    _connection_keywords = ('dsn', 'dbq', 'database', 'uid', 'pwd', 'autocommit', 'ansi', 'unicode_results', 'readonly', 'timeout', 'driver')

    def __init__(self, database, **kwargs):
        """\
        Initialize the Teradata connection object

        Keyword Arguments:
            dan string data source name
            uid string user ID for data source
            pwd string password for user id
            autocommit bool optional (default True)
            timeout int optional (default 0 - no timeout)
        """
        logger.info('SQLite initializer called')
        inputs = {'timeout': 30, 'driver': "SQLite3 ODBC Driver", 'autocommit': False}
        inputs.update({key: value for key, value in kwargs.items()})
        inputs['database'] = os.path.normpath(database)

        _connection_dict = {}

        for key in self.connection_keywords:
            if key in inputs:
                _connection_dict[key] = inputs.pop(key)

        inputs['_connection_dict'] = _connection_dict
        super().__init__(**inputs)

    def close(self):
        """\
        Closes the databse connection if open and flags the connection object as non-existant
        """
        logger.info('Teradata Close method called')
        try:
            self._connect.close()
        except (pyodbc.ProgrammingError, AttributeError):
            logger.info('Exception raised indicating connection was already closed')
            pass
        except:
            logger.critical("Unhandled excption encountered")
            raise
        finally:
            self._connect = None

    @property
    def conn_dict(self):
        """\
        Generates connection dictionary to help connection
        """
        logger.info('Connection Dictionary accessed')
        logger.debug(str(self._connection_dict.items()))
        return self._connection_dict.items()

    @property
    def connect(self):
        """\
        Returns a connection object, saves pre-existing connection or generates new connection if none exists
        """
        if self._connect is None:
            logger.info('New connection created')
            self._connect = pyodbc.connect(**self.conn_dict)
        logger.info('Connect property accessed')
        return self._connect

    @property
    def cursor(self):
        """\
        Creates a new database cursor for consumption
        """
        logger.info('New cursor created')
        return self.connect.cursor()

    def execute(self, sql, *args):
        logger.info('Access execute method called')
        logger.debug('SQL: \n {0}'.format(sql))
        if len(tuple((arg for arg in args))) > 0:
            logger.debug('Parameters: {0}'.format(', '.join(list([str(a) for a in args]))))
            return self.cursor.execute(sql, *args)
        else:
            return self.cursor.execute(sql)

    def executemany(self, sql, *args):
        logger.info('Access execute method called')
        logger.debug('SQL: \n {0}'.format(sql))
        logger.debug('Parameters: {0}'.format(', '.join(list([str(a) for a in args]))))
        return self.cursor.executemany(sql, *args)

