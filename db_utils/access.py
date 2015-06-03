# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:43:25 2015

@author: Robert Smith
"""

from db_utils.base import ABC_Database

import os
import pyodbc

import win32com.client
import win32api
import win32con
import pywintypes

import logging

logger = logging.getLogger(__name__)


class Access(ABC_Database):
    """\
    MS Access Database interaction object

    Members:
        driver string text for system installed driver
        dbq string full file path to access database

    Methods:
        db_execute executes SQL against stored database
        create_accdb creates new MS Access db and returns new Access object pointing to the database
    """

    def __init__(self, dbq=None, **kwargs):
        """\
        Initialize the AccessDB object

        Keyword Arguments:
            dbq string full file path to ms access database
            background_ind bool True indicates for Access to run in background, False runs Access in the foreground
            autocommit bool optional (default True)
            timeout int optional (default 0 - no timeout)

        """
        logger.info('Access object initialization')

        self.dbq = os.path.normpath(dbq)
        logger.debug('dbq member set to {0}'.format(dbq))

        reg_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\MSACCESS.EXE"
#       find local access EXE file
        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, reg_path)
        value = win32api.RegQueryValueEx(key, None)

        self.driver = kwargs.get("driver", "Microsoft Access Driver (*.mdb, *.accdb)")
        self.access_exe = os.path.normpath(value[0])
        self.autocommit = kwargs.get("autocommit", False)
        self.timeout = kwargs.get("timeout", 30)
        self._connect = None
        self._access_app = None

    def __del__(self):
        logger.info('Access object delete method called')
        self.close()
        for key,value in self.__dict__.items():
            setattr(self, key, None)

    def close(self):
        """\
        Closes the databse connection if open and flags the connection object as non-existant
        """
        logger.info('Access object close method called')
        try:
            self._connect.close()
        except (pyodbc.ProgrammingError, AttributeError):
            logger.error('Closing Exception Ignored -- No Connection Found')
            pass
        except Exception:
            logger.critical('Exception raised in Access.close()')
            raise
        finally:
            self._connect = None

    @property
    def connect(self):
        """\
        Returns a connection object, saves pre-existing connection or generates new connection if none exists
        """
        if self._connect is None:
            self._connect = pyodbc.connect(driver = self.driver, dbq = self.dbq, autocommit=self.autocommit, timeout=self.timeout)
            logger.info('Connection to database {0} created'.format(self.dbq))
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
            logger.debug('Parameters: {0}'.format(', '.join(list([a for a in args]))))
            return self.cursor.execute(sql, *args)
        else:
            return self.cursor.execute(sql)

    def executemany(self, sql, *args):
        logger.info('Access execute method called')
        logger.debug('SQL: \n {0}'.format(sql))
        logger.debug('Parameters: {0}'.format(', '.join(list([a for a in args]))))
        return self.cursor.executemany(sql, *args)

    @staticmethod
    def create_accdb(path, delete_if_exists=False):
        """\
        Creates new MS Access (*.accdb format) database when called.

        Keyword Arguments:
            path string full file path and name of database
            delete_if_exists bool (default False) if database exists and set to False will raise FileExistsError, if True current database will be deleted and new blank database will be created

        Return Value:
            New AccessDB object pointing to newly created database
        """
        logger.info('Create New Access Database Method Called')
        logger.debug('dbq = {0}'.format(path))
        if delete_if_exists:
            logger.debug('Delete If Exists Option Called')
            if os.path.isfile(path):
                logger.debug('Previous DB removed')
                os.remove(path)
        else:
            if os.path.isfile(path):
                logger.critical('Tried to overwrite existing database file without attempting to remove')
                raise FileExistsError

        access_app = win32com.client.DispatchEx("Access.Application")
        access_app.visible = False
        dbLangGeneral = ';LANGID=0x0409;CP=1252;COUNTRY=0'
        dbVersion = 128
        access_app.DBEngine.CreateDatabase(path, dbLangGeneral, dbVersion)
        access_app.quit()
        del access_app

        return Access(dbq = os.path.normpath(path))

    def compact_accdb(self):
        """\
        Compacts & Repairs existing MS Access database using command line argument.
        """
        logger.info('Compact Access Database method called')
        logger.debug('current database: {0}'.format(self.dbq))
        temp_file = os.path.split(self.dbq)
        temp_file = os.path.join(temp_file[0], '_'.join(['temp', temp_file[1]]))
        logger.debug('temp database: {0}'.format(temp_file))
        try:
            access_app = win32com.client.DispatchEx("Access.Application")
            access_app.visible = False
            access_app.DBEngine.CompactDatabase(self.dbq, temp_file)
        except pywintypes.com_error:
            logger.warning("Couldn't gain exclusive access to {0}".format(self.dbq))
            pass
        except Exception:
            logger.critical('Unhandled exception raised')
            raise
        finally:
            access_app.quit()
            del access_app

        if os.path.isfile(temp_file):
            logger.debug('Temp File exists -- deleting previous database and renaming compacted copy')
            os.remove(self.dbq)
            os.rename(temp_file, self.dbq)
        logger.debug('Compact operation completed')



if __name__ == '__main__':
     a = Access.create_accdb(r"C:\\Users\\A421356\\Desktop\\test.accdb", True)
     a.compact_accdb()
