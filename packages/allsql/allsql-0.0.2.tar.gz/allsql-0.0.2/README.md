# SQLITE3

### 1 - Import file
```
from allsql import Sqlite
```
### 2 - <i>Sqlite([local database])</i>
```
db = Sqlite('database.db')
```
### 3 - <i>db.create_database([database])</i>
```
db.create_database(db)
```
### 4 - <i>db.create_table([table],[columns type parameters])</i>
```
db.create_table('tb_test', 'id integer primary key autoincrement, name text, status integer')
```
### 5 - <i>db.truncate_table([table])</i>
```
db.truncate_table('tb_test')
```
### 6 - <i>db.drop_table([table])</i>
```
db.drop_table('tb_test')
```
### 7 - <i>db.insert([table],[columns],[values])</i>
```
db.insert('tb_test', 'name,status', '"Joe Climb",0')
```
### 8 - <i>db.update([table],[set],[where])</i>
```
db.update('tb_test', 'name = "Joe Caruzo", status = 0', 'status = 1')
```
### 9 - <i>db.delete([table],[where])</i>
```
db.delete('tb_test','id = 1, status = 0')
```
### 10 - <i>db.select([table],[columns],[where],[groupby],[orderby])</i>
```
print(db.select('tb_test','name,count(*)','id > 0, status != 0', 'name', 'name asc'))
```
### 11 - <i>db.sql([query])</i>
```
print(db.sql('select * from tb_test '))
```

# POSTGRES

### 1 - Import file
```
from allsql import Postgres
```
### 2 - <i>Postgres([user],[password],[host],[database])</i>
```
db = Postgres('<user>','<user_pass>','<host>','<dba>')
```
### 3 - <i>db.create_table([table],[columns type parameters])</i>
```
db.create_table('tb_test', 'id integer primary key generated always as identity, name text, status integer')
```
### 4 - <i>db.truncate_table([table])</i>
```
db.truncate_table('tb_test')
```
### 5 - <i>db.drop_table([table])</i>
```
db.drop_table('tb_test')
```
### 6 - <i>db.insert([table],[columns],[values])</i>
```
db.insert('tb_test', 'name,status', "'Joe Climb',0")
```
### 7 - <i>db.update([table],[set],[where])</i>
```
db.update('tb_test', 'name = "Joe Caruzo", status = 0', 'status = 1')
```
### 8 - <i>db.delete([table],[where])</i>
```
db.delete('tb_test','id = 1, status = 0')
```
### 9 - <i>db.select([table],[columns],[where],[groupby],[orderby])</i>
```
print(db.select('tb_test','name,count(*)','id > 0, status != 0', 'name', 'name asc'))
```
### 10 - <i>db.sql([query])</i>
```
print(db.sql('select * from tb_test '))
```

# ORACLE

### 1 - Import file
```
from allsql import Oracle
```
### 2 - <i>Oracle([user],[password],[host],[sid],[auto commit])</i>
```
db = Oracle('user','user_pass','127.0.0.1','orcl',True)
```
### 3 - <i>db.create_table([table],[columns type parameters])</i>
```
db.create_table('tb_test', 'id integer primary key autoincrement, name text, status integer')
```
### 4 - <i>db.truncate_table([table])</i>
```
db.truncate_table('tb_test')
```
### 5 - <i>db.drop_table([table])</i>
```
db.drop_table('tb_test')
```
### 6 - <i>db.insert([table],[columns],[values])</i>
```
db.insert('tb_test', 'name,status', '"Joe Climb",0')
```
### 7 - <i>db.update([table],[set],[where])</i>
```
db.update('tb_test', 'name = "Joe Caruzo", status = 0', 'status = 1')
```
### 8 - <i>db.delete([table],[where])</i>
```
db.delete('tb_test','id = 1, status = 0')
```
### 9 - <i>db.select([table],[columns],[where],[groupby],[orderby])</i>
```
print(db.select('tb_test','name,count(*)','id > 0, status != 0', 'name', 'name asc'))
```
### 10 - <i>db.sql([query])</i>
```
print(db.sql('select * from tb_test '))
```

# MYSQL

### 1 - Import file
```
from allsql import Mysql
```
### 2 - <i>Mysql([user],[password],[host],[sid])</i>
```
db = Mysql('<user>','<user_pass>','<host>','<dba>')
```
### 3 - <i>db.create_table([table],[columns type parameters])</i>
```
db.create_table('tb_test', 'id integer primary key auto_increment, name text, status integer')
```
### 4 - <i>db.truncate_table([table])</i>
```
db.truncate_table('tb_test')
```
### 5 - <i>db.drop_table([table])</i>
```
db.drop_table('tb_test')
```
### 6 - <i>db.insert([table],[columns],[values])</i>
```
db.insert('tb_test', 'name,status', '"Joe Climb",0')
```
### 7 - <i>db.update([table],[set],[where])</i>
```
db.update('tb_test', 'name = "Joe Caruzo", status = 0', 'status = 1')
```
### 8 - <i>db.delete([table],[where])</i>
```
db.delete('tb_test','id = 1, status = 0')
```
### 9 - <i>db.select([table],[columns],[where],[groupby],[orderby])</i>
```
print(db.select('tb_test','name,count(*)','id > 0, status != 0', 'name', 'name asc'))
```
### 10 - <i>db.sql([query])</i>
```
print(db.sql('select * from tb_test '))
```