# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 13:08:16 2015

@author: Robert Smith
"""


from db_utils.base import ABC_Database

import pyscopg2 as dbc

import logging

logger = logging.getLogger(__name__)


class PostgreSQL(ABC_Database):
    """\
    PostgreSQL Database interaction object

    Members:
        driver string text for system installed driver
        dbq string full file path to access database

    Methods:
        db_execute executes SQL against stored database
        create_accdb creates new MS Access db and returns new Access object pointing to the database
    """
    _connect = None

    def __init__(self, dsn, uid, pwd, **kwargs):
        """\
        Initialize the PostgreSQL connection object

        Keyword Arguments:
            dan string data source name
            uid string user ID for data source
            pwd string password for user id
            autocommit bool optional (default True)
            timeout int optional (default 0 - no timeout)
        """
        logger.info('PostgreSQL initializer called')
        input_dict = {key: value for key, value in kwargs.items()}
        input_dict['dsn'] = str(dsn)
        input_dict['uid'] = str(uid)
        input_dict['pwd'] = str(pwd)
        input_dict['autocommit'] = False
        input_dict['timeout'] = 30
        super().__init__(**input_dict)

    def close(self):
        """\
        Closes the databse connection if open and flags the connection object as non-existant
        """
        logger.info('PostgreSQL Close method called')
        try:
            self._connect.close()
        except (dbc.ProgrammingError, AttributeError):
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
        output = {"dsn": self.dsn, "uid": self.uid, "pwd": self.pwd, "autocommit": self.autocommit, "timeout": self.timeout}
        for key, value in output.items():
            if value is None:
                del output[key]
        logger.debug(str(output))
        return output

    @property
    def sqlalchemy_str(self):
        return 'postgresql+psycopg2://{uid}:{pwd}@localhost:5432/{uid}'.format(**self.conn_dict)

    @property
    def sqlalchemy_connect_args(self):
        return dict({k: v for k, v in self.conn_dict.items() if k not in ('dsn', 'uid', 'pwd')})

    @property
    def connect(self):
        """\
        Returns a connection object, saves pre-existing connection or generates new connection if none exists
        """
        if self._connect is None:
            logger.info('New connection created')
            self._connect = dbc.connect(**self.conn_dict)
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

#    def execute_to_txt(self, sql, filepath, *args, **kwargs):
#        import csv
#        import os
#        dialect = kwargs.get('dialect', 'excel-tab')
#        header = kwargs.get('header', True)
#
#        qry = self.execute(sql, *args)
#        fieldnames = list([v[0] for v in qry.description])
#        with open(os.path.normpath(filepath), mode='r', newline='') as fp:
#            wr = csv.DictWriter(fp, fieldnames=fieldnames, dialect=dialect)
#            if header:
#                wr.writeheader()
#            for row in qry:
#                wr.writerows(row)

