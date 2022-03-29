mysql_extract = ('''
  SELECT mysql_column_1, mysql_column_2, mysql_column_3
  FROM mysql_table
''')

mysql_insert = ('''
  INSERT INTO table (column_1, column_2, column_3)
  VALUES (?, ?, ?)  
''')
# exporting queries
class SqlQuery:
  def __init__(self, extract_query, load_query):
    self.extract_query = extract_query
    self.load_query = load_query
# create instances for SqlQuery class

mysql_query = SqlQuery(mysql_extract, mysql_insert)

# store as list for iteration
mysql_queries = [mysql_query]


