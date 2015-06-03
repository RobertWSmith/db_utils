# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 00:18:18 2015

@author: Robert Smith
"""

from db_utils.base import ABC_Database


import pyodbc


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
        self.dsn = str(dsn)
        self.uid = str(uid)
        self.pwd = str(pwd)

        self.driver = kwargs.get("driver", None)

        self.autocommit = kwargs.get("autocommit", None)
        self.timeout = kwargs.get("timeout", None)
        self._connect = None

    def __del__(self):
        self.close()
        for key,value in self.__dict__.items():
            setattr(self, key, None)

    def close(self):
        """\
        Closes the databse connection if open and flags the connection object as non-existant
        """
        try:
            self._connect.close()
        except (pyodbc.ProgrammingError, AttributeError):
            pass
        except:
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
        return output

    @property
    def connect(self):
        """\
        Returns a connection object, saves pre-existing connection or generates new connection if none exists
        """
        if self._connect is None:
            self._connect = pyodbc.connect(**self.conn_dict)
        return self._connect

    @property
    def cursor(self):
        """\
        Creates a new database cursor for consumption
        """
        return self.connect.cursor()


