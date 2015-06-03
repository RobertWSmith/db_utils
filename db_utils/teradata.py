# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 00:18:18 2015

@author: Robert Smith
"""

from db_utils.base import ABC_Database

import pyodbc

import logging

logger = logging.getLogger(__name__)


class Teradata(ABC_Database):
    """\
    MS Access Database interaction object

    Members:
        driver string text for system installed driver
        dbq string full file path to access database

    Methods:
        db_execute executes SQL against stored database
        create_accdb creates new MS Access db and returns new Access object pointing to the database
    """

    def __init__(self, dsn, uid, pwd, **kwargs):
        """\
        Initialize the Teradata connection object

        Keyword Arguments:
            dan string data source name
            uid string user ID for data source
            pwd string password for user id
            autocommit bool optional (default True)
            timeout int optional (default 0 - no timeout)
        """
        logger.info('Teradata initializer called')
        self.dsn = str(dsn)
        self.uid = str(uid)
        self.pwd = str(pwd)
        logger.debug('dsn={dsn}, uid={uid}, pwd={pwd}'.format(dsn=self.dsn, uid=self.uid, pwd=self.pwd))

        self.driver = kwargs.get("driver", None)
        self.autocommit = kwargs.get("autocommit", None)
        self.timeout = kwargs.get("timeout", None)
        self._connect = None

    def __del__(self):
        logger.info('Teradata Delete method called')
        self.close()
        for key,value in self.__dict__.items():
            setattr(self, key, None)

    def close(self):
        """\
        Closes the databse connection if open and flags the connection object as non-existant
        """
        logger.info('Teradata Close method called')
        try:
            self._connect.close()
        except (pyodbc.ProgrammingError, AttributeError):
            logger.warning('Exception raised indicating connection was already closed')
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
        output = {"dsn": self.dsn, "uid": self.uid, "pwd": self.pwd, "autocommit": self.autocommit, "timeout": self.timeout}
        for key, value in output.items():
            if value is None:
                del output[key]
        logger.debug(str(output))
        return output

    @property
    def connect(self):
        """\
        Returns a connection object, saves pre-existing connection or generates new connection if none exists
        """
        if self._connect is None:
            logger.info('New connection created')
            self._connect = pyodbc.connect(**self.conn_dict)
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

