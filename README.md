# 512_BigBucks_Automation
This is for FINTECH 512 Group Project Automation Process For Updating Stock Price &amp; SP500

We will hold d automation process on [Pipedream](https://pipedream.com)

Simply run following codes to update yesterday data : 
```python
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
```

