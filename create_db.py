import sqlite3
conn = sqlite3.connect('trading_db.db')
c = conn.cursor()

c.execute("DROP TABLE users")
c.execute("DROP TABLE accounts")
c.execute("DROP TABLE portfolios")

c.execute("""CREATE TABLE 'users' (
'id' INTEGER,
'username' VARCHAR,
'password' VARCHAR,
'name' VARCHAR,
'permission_level' INTEGER,
PRIMARY KEY ('id')
)""")

c.execute("""CREATE TABLE 'accounts' (
'id' INTEGER,
'user_id' INTEGER,
'account_number' VARCHAR,
'balance' REAL,
FOREIGN KEY ('user_id') REFERENCES users(id),
PRIMARY KEY ('id')
)""")

c.execute("""CREATE TABLE 'portfolios' (
'id' INTEGER,
'user_id' INTEGER,
'symbol' VARCHAR,
'price' REAL,
'quantity', INT,
FOREIGN KEY ('user_id') REFERENCES user(id),
PRIMARY KEY ('id')
)""")

conn.commit()
