# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:43:12 2015

@author: Robert Smith
"""

from abc import ABC

class ABC_Database(ABC):
    """\
    Database Connection / Cursor / Execute Abstract Base Class. Defines required implementation elements.
    """

    def __init__(self, **kwargs):
        raise NotImplementedError

    def __del__(self):
        raise NotImplementedError

    def close(self):
        """\
        Closes the databse connection if open and flags the connection object as non-existant
        """
        raise NotImplementedError

    def connect(self):
        """\
        Returns a connection object, saves pre-existing connection or generates new connection if none exists
        """
        raise NotImplementedError

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

