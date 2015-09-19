import requests

class Markit:
	def __init__(self):
		self.lookup_url = "http://dev.markitondemand.com/Api/v2/Lookup/json?input="
		self.quote_url = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol="

	def company_search(self,string):
		r = requests.get(self.lookup_url+string)
		return r.json()

	def get_quote(self,string):
		r = requests.get(self.quote_url+string)
		try:
		#r.json().get("LastPrice"):
		#admin ranking isn't fully working, for some reason API does not return
		#all the LastPrices. Maybe change so that function goes through all the id's
		#and calculates their portfolios like for users side. then add those in dict/list.
			return r.json().get("LastPrice")
		except ValueError:
			return 0

	def get_company_data(self, string):
		r = requests.get(self.quote_url+string)
		return r.json()

# search = Markit()
# print(search.company_search("Apple"))
# print(search.get_quote("GOOGL"))
# print(search.get_quote("Gohbg"))
