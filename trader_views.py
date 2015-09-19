import os
from wrapper import Markit
from prettytable import PrettyTable

class View:
    def __init__(self):
        self.api = Markit()

    def clear(self):
        os.system("clear")

    def signin(self):
        self.clear()
        return input("""Welcome to BA Stock Trader Game. Press 1 or 2:\n
1: Login
2: Create an account
\n""")

    def get_username(self):
        return input("Username: ")

    def get_password(self):
        return input("Password: ")

    def get_fullname(self):
        return input("Full name: ")

    def creating_account(self):
        print("Please fill out these fields: ")

    def wrong_username_or_password(self):
        print("Wrong username or password")

    def invalid_choice(self):
        print("Invalid choice. Please type again. ")

    def username_exists(self):
        print("Username already exists.")

    def welcome_admin(self):
        print("Welcome back admin. Below are the TOP 10 portfolios: ")

    def user_menu(self):
        return input("""What would you like to do? Please press number:
    1: See my dashboard
    2: Search for stocks
    3: Buy stocks
    4: Sell stocks
    5: Quit
""")

    def press_number(self):
        self.clear()
        print("Invalid choice. Please press a number between 1 and 5.")

    def search_type(self):
        return input("""Please press number:
1: Search by company name
2: Search by company symbol
""")

    def search_by_company(self):
        return input("Please type company name: ")

    def company_not_found(self):
        print()
        print("Company not found.")
        print()

    def search_instructions(self):
        print()
        print("""Search again with the company symbol, if you want to see market data.
""")

    def search_by_symbol(self):
        return input("Please type company symbol: ")

    def company_info(self, companies):
        self.clear()
        for company in companies:
            print("Name: {} Symbol: {} Exchange: {}".format(company['Name'], company['Symbol'], company['Exchange']))

    def company_data(self, data):
        self.clear()
        x = PrettyTable(["Symbol", "Price", "Open", "High", "Low", "Change%", "ChangePercentYTD"])
        x.align["Symbol"] = "l"
        x.padding_width = 1
        x.add_row([data['Symbol'], data['LastPrice'], data['Open'], data['High'],
        data['Low'], data['ChangePercent'], data['ChangePercentYTD']])
        print(x)

    def leaderboard(self, dic):
        self.clear()
        x = PrettyTable(["User ID", "Current value", "Price paid", "Profit/Loss"])
        x.align["User ID"] = "l"
        x.padding_width = 1
        for key, value in dic.items():
            x.add_row([key, round(value[0],2), round(value[1],2), round(value[2],2)])
        print(x.get_string(start=0, end=9, sortby="Profit/Loss", reversesort=True))

    def current_value(self, symbol, value):
        print("Last price for {} is ${}".format(symbol, value))
        print()

    def get_balance(self, balance):
        self.clear()
        print("Your current account balance is ${}.".format(balance))
        print()

    def get_quantity(self):
        return input("How many stocks would like to purchase? ")

    def get_total_price(self, total_price):
        print()
        print("The total price will be ${}".format(total_price))

    def insufficient_funds(self):
        print("insufficient funds.")

    def confirm_purchase(self):
        print()
        return input("Press 'c' to confirm, 'q' to quit: ")

    def stocks_to_be_sold(self):
        return input("Give the symbol of the stocks you want to sell: ")

    def show_number_of_stocks(self, symbol, number_of_stocks):
        print()
        print("You have {} {} stocks available. ".format(number_of_stocks[0], symbol))
        print()

    def how_many_for_sale(self):
        return input("How many stocks do you want to sell? ")

    def invalid_number(self):
        print("Invalid number of stocks. Please type again: ")

    def list_all_accounts(self, accounts):
        self.clear()
        for account in accounts:
            print("id: {} username: {} name: {} account: {} balance: {}".format(account[0],
            account[1], account[3], account[7], account[8]))

    def list_all_portfolios(self, portfolios):
        for portfolio in portfolios:
            print("id: {} symbol: {} price: {} quantity: {}".format(portfolio[1],
            portfolio[2], portfolio[3], portfolio[4]))

    def show_profit_loss(self, profit_loss):
        print("Your profit/loss is ${}".format(profit_loss))



    def print_current_portfolio_value(self, value, paid, profit):
        print("""
    Portfolio value: ${}
    Purchase price ${},
    Profit/loss: ${}
    """.format(value, paid, profit))
