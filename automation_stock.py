import pendulum
import requests
import yfinance as yf

SUPABASE_URL = ""
KEYS = ""

def get_all_symbols():
	api_url = SUPABASE_URL + "/rest/v1/" + "Stock_Information"

	parameters =  {"apikey":KEYS}

	response = requests.get(url = api_url, params = parameters)
	data = response.json()

	symbols = []

	for d in data:
		symbols.append(d['stock_symbol'])

	return symbols


def store_stock_price_data():
	symbol_list = get_all_symbols()

	# get today's date
	now = pendulum.now()
	one_day_ago = str(now.subtract(days=1).date())

	check_Saturday = str(now.end_of('week').subtract(days=1).date())
	check_Sunday = str(now.end_of('week').date())

	# print(check_Sunday)
	# print(check_Saturday)
	# print(one_day_ago)

	if ((one_day_ago != check_Saturday) and (one_day_ago != check_Sunday)):
	
		all_data = {}
		for stock_symbol in symbol_list:
			base_url = 'https://www.alphavantage.co/query?'
			params = {"function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": stock_symbol, "outputsize" : "compact","apikey": "9Q91BWGMOE13WOR3"}
			
			response = requests.get(base_url, params=params)
			data = response.json() # dict
			# store all data 
			all_data[stock_symbol] = data['Time Series (Daily)'][one_day_ago]

		# set to db format 
		for stock_symbol,p in all_data.items():
			update_data = update_stock_daily_price(stock_symbol, one_day_ago, p['1. open'], p['2. high'], p['3. low'], p['4. close'], p['5. adjusted close'], p['6. volume'])
			#supabase_insert_function(update_data[0], update_data[1])
			print(update_data)
	else:
		print("It's on weekend! No need to update!")

# daily price
def update_stock_daily_price(stock_symbol : str, date, open_ : float, high : float, low : float, close : float, adjusted_close : float, volume : int):
	stock_price = {}
	stock_price["stock_symbol"] = stock_symbol
	stock_price["date"] = date
	stock_price["open"] = open_
	stock_price["high"] = high
	stock_price["low"] = low
	stock_price["close"] = close
	stock_price["adjusted_close"] = adjusted_close
	stock_price["volume"] = volume

	return "Stock_Price_Daily_Data", stock_price

def supabase_insert_function(table_name : str, data_to_insert : dict)->str:
	"""
	excute rest api command to insert data to supabase 
	"""
	try:
		# route to table
		api_url = SUPABASE_URL + "/rest/v1/" + table_name

		parameters =  {"apikey": KEYS}

		response = requests.post(url = api_url, params = parameters, json = data_to_insert)

	except:
		print("Fail to implement supabse insert function")

# SP500 updates goes here
def sp500():
	# get today's date
	now = pendulum.now()
	one_day_ago = str(now.subtract(days=1).date())

	check_Saturday = str(now.end_of('week').subtract(days=1).date())
	check_Sunday = str(now.end_of('week').date())
	check_next_Monday = str(now.end_of('week').add(days=1).date())
	# print(check_Sunday)
	# print(check_next_Monday)

	data = yf.download(tickers= "^GSPC", period='1d')

	dict_sp500 = {}
	# print(data)

	date_time = str(data.index[0]).split()[0]

	index_ = data.iloc[0]["Adj Close"]

	dict_sp500[date_time] = float(index_)

	real_sp500 = {}
	for k,v in dict_sp500.items():
		if (now.date() != check_Sunday and now.date() != check_next_Monday):
			real_sp500["date"] = k
			real_sp500["close"] = v


	return "SP500_Index", real_sp500

def update_sp500_yesterday():
	tmp = sp500()
	#supabase_insert_function(tmp[0], tmp[1])
	print(tmp)

def main():
	try: 
		store_stock_price_data()
	except:
		print("Fail to update stock price")

	try: 
		update_sp500_yesterday()
	except:
		print("Fail to update SP500")


if __name__ == '__main__':
	main()








