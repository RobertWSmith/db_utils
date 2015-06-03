# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:43:25 2015

@author: Robert Smith
"""

from db_utils.base import ABC_Database
#from mixins import ReprMixin

import os
import pyodbc



import win32com.client
import win32api
import win32con
import pywintypes



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
        self.dbq = os.path.normpath(dbq)
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
        except Exception:
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
        return self._connect

    @property
    def cursor(self):
        """\
        Creates a new database cursor for consumption
        """
        return self.connect.cursor()

    def execute(self, sql, *args):
        if len(tuple((arg for arg in args))) > 0:
            return self.cursor.execute(sql, *args)
        else:
            return self.cursor.execute(sql)

    def executemany(self, sql, *args):
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
        if delete_if_exists:
            if os.path.isfile(path):
                os.remove(path)
        else:
            if os.path.isfile(path):
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
        temp_file = os.path.split(self.dbq)
        temp_file = os.path.join(temp_file[0], '_'.join(['temp', temp_file[1]]))
        try:
            access_app = win32com.client.DispatchEx("Access.Application")
            access_app.visible = False
            access_app.DBEngine.CompactDatabase(self.dbq, temp_file)
        except pywintypes.com_error:
            pass
        except Exception:
            raise
        finally:
            access_app.quit()
            del access_app

        if os.path.isfile(temp_file):
            os.remove(self.dbq)
            os.rename(temp_file, self.dbq)



if __name__ == '__main__':
     a = Access.create_accdb(r"C:\\Users\\A421356\\Desktop\\test.accdb", True)
     a.compact_accdb()
