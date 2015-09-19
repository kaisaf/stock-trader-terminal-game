from trader_models import TradingUserDB, User, Player, Admin, Account
from trader_views import View
from wrapper import Markit


class TraderController:
    def __init__(self):
        self.view = View()
        self.db = TradingUserDB()
        self.api = Markit()

    def login(self):
        user_name = self.view.get_username()
        password = self.view.get_password()
        return user_name, password

    def get_id(self, user_name):
        user_id = self.db.user_id_check(user_name)
        return user_id[0]

    def create_account(self):
        self.view.creating_account()
        user_name, password = self.login()
        user_id = self.db.user_id_check(user_name)
        if user_id == None:
            name = self.view.get_fullname()
            new_user = Player(user_name, password, name)
            self.db.add_user(new_user)
            user_id = self.db.user_id_check(user_name)
            new_account = Account(user_id)
            self.db.add_account(new_account)
        else:
            self.view.username_exists()
            self.create_account()
        return user_name, password

    def current_balance(self, user_name):
        balance = self.db.get_account_balance(self.db.user_id_check(user_name))
        self.view.get_balance(balance[0])
        return balance

    def run(self):
        signin = self.view.signin()
        if signin == "1":
            user_name, password = self.login()
            validate = self.db.signin(user_name, password)
            while validate == None:
                self.view.wrong_username_or_password()
                user_name, password = self.login()
                validate = self.db.signin(user_name, password)
            if validate[1] == 1:
                self.view.welcome_admin()
                dict_leaders = {}
                portfolios = self.db.get_all_portfolios()
                for portfolio in portfolios:
                    key = portfolio[1]
                    if key in dict_leaders:
                        value, paid, profit = self.db.one_portfolio_value(portfolio)
                        l = dict_leaders.get(key)
                        for idx, num in enumerate(l):
                            if idx == 0:
                                value = num + value
                            elif idx == 1:
                                paid = num + paid
                            else:
                                profit = num + profit
                        dict_leaders[key] = [value, paid, profit]
                    else:
                        value, paid, profit = self.db.one_portfolio_value(portfolio)
                        dict_leaders[key] = [value, paid, profit]
                self.view.leaderboard(dict_leaders)
        elif signin == "2":
            user_name, password = self.create_account()
        else:
            self.view.invalid_choice()
        user_id = self.get_id(user_name)

        while True:
            action = self.view.user_menu()
            if action == "1":
                self.current_balance(user_name)
                portfolio = self.db.get_own_portfolio(user_id)
                self.view.list_all_portfolios(portfolio)
                value, paid, profit = self.db.current_portfolio_value(portfolio)
                self.view.print_current_portfolio_value(value, paid, profit)
            elif action == "2":
                search_type = self.view.search_type()
                if search_type == "1":
                    company = self.view.search_by_company()
                    info = self.view.company_info(self.api.company_search(company))
                    if self.api.company_search(company) == []:
                        self.view.company_not_found()
                    else:
                        self.view.search_instructions()
                elif search_type == "2":
                    symbol = self.view.search_by_symbol()
                    self.api.get_company_data(symbol)
                    self.view.company_data(self.api.get_company_data(symbol))
                    self.view.current_value(symbol, self.api.get_quote(symbol))
            elif action == "3":
                balance = self.current_balance(user_name)
                symbol = self.view.search_by_symbol()
                price = self.api.get_quote(symbol)
                if price == None:
                    self.view.company_not_found()
                else:
                    self.view.current_value(symbol, price)
                    quantity = self.view.get_quantity()
                    total_price = price * float(quantity)
                    self.view.get_total_price(total_price)
                    if total_price > balance[0]:
                        self.view.insufficient_funds()
                    else:
                        confirm = self.view.confirm_purchase()
                        if confirm.lower() == "c":
                            self.db.add_to_portfolio(user_id, symbol, price, quantity)
                            self.db.update_account(total_price*-1, user_id)
                            self.current_balance(user_name)
                        elif confirm == "q":
                            continue
            elif action == "4":
                symbol = self.view.stocks_to_be_sold()
                price = self.api.get_quote(symbol)
                stocks_with_symbol = self.db.get_from_portfolio(symbol, user_id)
                self.view.list_all_portfolios(stocks_with_symbol)
                number_of_stocks = self.db.get_number_of_stocks_available(symbol, user_id)
                if number_of_stocks[0][0] == None:
                    self.view.company_not_found()
                    continue
                self.view.show_number_of_stocks(symbol, number_of_stocks[0])
                sell = int(self.view.how_many_for_sale())
                while sell > number_of_stocks[0][0] or sell < 1:
                    self.view.invalid_number()
                    sell = int(self.view.how_many_for_sale())
                price_paid = self.db.subtract_stocks(sell, stocks_with_symbol)
                profit = sell * price
                profit_loss = profit - price_paid
                self.view.show_profit_loss(profit_loss)
                self.db.update_account(profit, user_id)
                self.db.remove_zero_stocks()
            elif action == "5":
                break
            else:
                self.view.press_number()






trader = TraderController()
trader.run()
