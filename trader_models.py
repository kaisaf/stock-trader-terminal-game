import sqlite3
from datetime import date
from random import randint
from wrapper import Markit
conn = sqlite3.connect('trading_db.db')
c = conn.cursor()

class TradingUserDB:
    def __init__(self):
        self.api = Markit()

    def signin(self, name, password):
        user = c.execute("SELECT id, permission_level FROM users WHERE username=(?) and password=(?)", (name, password))
        user = c.fetchone()
        return user

    def user_id_check(self, user_name):
        c.execute("SELECT id FROM users WHERE username=(?)", (user_name,))
        account = c.fetchone()
        return account

    def add_user(self, user):
        c.execute("INSERT INTO users(username, password, name, permission_level) VALUES(?,?,?,?)", (user.username, user.password, user.name, user.permission_level))
        conn.commit()

    def add_account(self, account):
        c.execute("INSERT INTO accounts(user_id, account_number, balance) VALUES(?,?,?)", (account.user_id, account.account_number, account.balance))
        conn.commit()

    def get_account_balance(self, id):
        c.execute("SELECT balance FROM accounts WHERE user_id=(?)", (id))
        balance = c.fetchone()
        return balance

    def update_account(self, change, user_id):
        c.execute("UPDATE accounts SET balance=balance+(?) WHERE user_id=(?)", (change, user_id))
        conn.commit()

    def get_all_user_accounts(self):
         c.execute("SELECT * FROM users INNER JOIN accounts ON users.id=accounts.user_id")
         accounts = c.fetchall()
         return accounts

    def add_to_portfolio(self, user_name, symbol, price, quantity):
        c.execute("INSERT INTO portfolios(user_id, symbol, price, quantity) VALUES(?,?,?,?)", (user_name, symbol, price, quantity))
        conn.commit()

    def update_portfolio(self, portfolio_id, user_id, number_of_stocks):
        c.execute("UPDATE portfolios SET quantity=quantity-(?) WHERE id=(?) and user_id=(?)", (number_of_stocks, portfolio_id, user_id))
        conn.commit()

    def remove_zero_stocks(self):
        c.execute("DELETE FROM portfolios WHERE quantity=(?)", (0,))
        conn.commit()

    def subtract_stocks(self, number_of_stocks, stocks_with_symbol):
        price_paid = 0
        while number_of_stocks > 0:
            for row in stocks_with_symbol:
                if number_of_stocks > int(row[4]):
                    number_of_stocks -= int(row[4])
                    price_paid += row[3] * int(row[4])
                    self.update_portfolio(row[0], row[1], int(row[4]))
                else:
                    self.update_portfolio(row[0], row[1], number_of_stocks)
                    price_paid += row[3] * number_of_stocks
                    number_of_stocks = 0
        return price_paid

    def get_all_portfolios(self):
        c.execute("SELECT * FROM portfolios")
        portfolios = c.fetchall()
        return portfolios

    def get_own_portfolio(self, user_id):
        c.execute("SELECT * FROM portfolios WHERE user_id=(?)", (user_id,))
        portfolio = c.fetchall()
        return portfolio

    def get_from_portfolio(self, symbol, user_id):
        c.execute("SELECT * FROM portfolios WHERE symbol=(?) and user_id=(?)", (symbol, user_id))
        portfolios = c.fetchall()
        return portfolios

    def get_number_of_stocks_available(self, symbol, user_id):
        c.execute("SELECT sum(quantity) FROM portfolios WHERE symbol=(?) and user_id=(?)", (symbol, user_id))
        portfolios = c.fetchall()
        return portfolios

    def current_portfolio_value(self, portfolio):
        value = 0.0
        paid = 0.0
        for row in portfolio:
            value += self.api.get_quote(row[2]) * float(row[4])
            paid += row[3] * float(row[4])
        profit = value - paid
        return value, paid, profit

    def one_portfolio_value(self, portfolio):
        value = 0.0
        paid = 0.0
        value += self.api.get_quote(portfolio[2]) * float(portfolio[4])
        paid += portfolio[3] * float(portfolio[4])
        profit = value - paid
        return value, paid, profit


class User:
    def __init__(self, username, password, name):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.account_created = date.today()

    def __str__(self):
        return self.username

class Player(User):
    def __init__(self, username, password, name):
        User.__init__(self, username, password, name)
        self.permission_level = 2

class Admin(User):
    def __init__(self, username, password, name):
        User.__init__(self, username, password, name)
        self.permission_level = 1

class Account:
    def __init__(self, user, balance=100000):
        self.user_id = user[0]
        self.account_number = str(user[0]) + str(randint(0, 9999))
        self.balance = balance
