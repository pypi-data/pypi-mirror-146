# pyftpdlibsqladdon
 Module for implementing FTP users in pyftpdlib through a SQL server

### Installation
```
pip install pyftpdlibsqladdon
```

### Get started

How to start pyftpdlib with user support via SQL

```Python
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlibsqladdon import DummySqlAuthorizer

def main():
    #define DummySqlAuthorizer
    authorizer = DummySqlAuthorizer()
    #add SQL server configuration
    authorizer.add_sql_config('host_ip','database','sql_user','sql_password')
    #add SQL column names where data is stored
    authorizer.add_sql_query('table','user_column','password_column','home_path_column','permission_colum')
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('', 21), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
```

### Considerations

This authorizer cannot be used in conjunction with DummyAuthorizer, as it overwrites the virtual table of users with those obtained from the database.
