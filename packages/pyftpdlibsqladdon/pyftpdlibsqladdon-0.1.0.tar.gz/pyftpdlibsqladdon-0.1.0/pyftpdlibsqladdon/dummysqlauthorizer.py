import os
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib._compat import unicode
from .client import SqlClient

class DummySqlAuthorizer(DummyAuthorizer):
    def add_sql_config(self, host, database, dbuser, dbpassword):
        dic = {'host': str(host),
               'database': str(database),
               'user': str(dbuser),
               'password': str(dbpassword)
               }
        self.user_table["sql_server_config"] = dic

    def add_sql_query(self, table, user, password, home, permissions):
        dic = {'table': str(table),
               'user': str(user),
               'password': str(password),
               'home': str(home),
               'permissions': str(permissions)
               }
        self.user_table["sql_query_config"] = dic


    def validate_authentication(self, username, password, handler):
        """Raises AuthenticationFailed if supplied username and
        password don't match the stored credentials, else return
        None.
        """
        if username == "sql_query_config":
            return None
        if username == "sql_server_config":
            return None
        try:
            userDataRow = SqlClient.sqlUser(username,self.user_table["sql_server_config"],self.user_table["sql_query_config"])
        except KeyError:
            msg = "Sql configuration doesn't exist"
            print("Error on DummySqlAuthorizer: " + msg)
            raise AuthenticationFailed(msg)
        msg = "User doesn't exist"
        if not userDataRow:
            raise AuthenticationFailed(msg)
        userData = userDataRow[0]
        password = userData[1]
        homedir = userData[2]
        perm = userData[3]
        msg_login = "Login successful."
        msg_quit = "Goodbye."
        if not isinstance(homedir, unicode):
            homedir = homedir.decode('utf8')
        if not os.path.isdir(homedir):
            raise ValueError('no such directory: %r' % homedir)
        homedir = os.path.realpath(homedir)
        self._check_permissions(username, perm)
        dic = {'pwd': str(password),
               'home': homedir,
               'perm': perm,
               'operms': {},
               'msg_login': str(msg_login),
               'msg_quit': str(msg_quit)
               }
        self.user_table[username] = dic
        msg = "Authentication failed."
        if not self.has_user(username):
            if username == 'anonymous':
                msg = "Anonymous access not allowed."
            raise AuthenticationFailed(msg)
        if username != 'anonymous':
            if self.user_table[username]['pwd'] != password:
                raise AuthenticationFailed(msg)
