datawarehouse_name = 'your_datawarehouse_name'

# sql-server (target db, datawarehouse)
datawarehouse_db_config = {
  'Trusted_Connection': 'yes',
  'driver': '{SQL Server}',
  'server': 'datawarehouse_sql_server',
  'database': '{}'.format(datawarehouse_name),
  'user': 'your_db_username',
  'password': 'your_db_password',
  'autocommit': True,
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
#list
mysql_db_config = [
  {
    'user': 'your_user_1',
    'password': 'your_password_1',
    'host': 'db_connection_string_1',
    'database': 'db_1',
  },
  {
    'user': 'your_user_2',
    'password': 'your_password_2',
    'host': 'db_connection_string_2',
    'database': 'db_2',
  },
]