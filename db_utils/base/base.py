# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:43:12 2015

@author: Robert Smith
"""

from abc import ABC

import logging

logger = logging.getLogger(__name__)

class ABC_Database(ABC):
    """\
    Database Connection / Cursor / Execute Abstract Base Class. Defines required implementation elements.
    """
    _connect = None
    _connection_keywords = ('dsn', 'dbq', 'database', 'uid', 'pwd', 'autocommit', 'ansi', 'unicode_results', 'readonly', 'timeout', 'driver')

    def __init__(self, **kwargs):
        logger.debug('Base Initializer Called')
        for key, value in kwargs.items():
            logger.debug('Set - Key:{key} / Value:{value}'.format(key=key, value=value))
            setattr(self, key, value)

    def __del__(self):
        logger.debug('Base Delete method called')
        self.close()
        for key, value in self.__dict__.items():
            setattr(self, key, None)

    def close(self):
        """\
        Closes the databse connection if open and flags the connection object as non-existant
        """
        logger.debug('Base Close method called')
        self.connect.close()
        self._connect = None

    @property
    def connection_keywords(self):
        return self._connection_keywords

    @property
    def connect(self):
        """\
        Returns a connection object, saves pre-existing connection or generates new connection if none exists
        """
        raise NotImplementedError

    @property
    def cursor(self):
        """\
        Creates a new database cursor for consumption
        """
        raise NotImplementedError

    def execute(self, sql, *args):
        """\
        Execute SQL & arguments as provided.
        """
        raise NotImplementedError

    def executemany(self, sql, *args):
        """\
        Execute SQL & a sequence of arguments.
        """
        raise NotImplementedError

