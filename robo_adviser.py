from dotenv import load_dotenv
import json
import os
import requests
import csv
from datetime import datetime
from IPython import embed

load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable
line = "----------------------------------------------------------------------------"
# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY") or "OOPS. Please set an environment variable named 'ALPHAVANTAGE_API_KEY'."

def stock_dict(symbol):
    response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol+ "&outputsize=compact&apikey=" + api_key)
    response_data = json.loads(response.text)
    return response_data
# TODO: issue a "GET" request to the specified url, and store the response in a variable
# TODO: assemble the request url to get daily data for the given stock symbol
def input_stocks(stock_count):
    error_msg = {
        "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY."
    }
    symbol = input("Input Stock Ticker# " + str(i+1) + ": ") #TODO: capture user input
    message = stock_dict(symbol)
    while message == error_msg:
        print(error_msg)
        symbol = input("Input Stock Ticker# " + str(i+1) + ": ")
        message = stock_dict(symbol)
    return symbol

def write_csv(filename,stocks=[]):
   filepath = os.path.join(os.path.dirname(__file__),"data",filename)
   with open(filepath, "w") as csv_file:
       writer = csv.DictWriter(csv_file,fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
       writer.writeheader() # uses fieldnames set above
       for s in stocks:
           writer.writerow(s)

# see: https://www.alphavantage.co/documentation/#daily
# TODO: parse the JSON response
stock_count = input("Please enter the number of stocks you want to input ")
stocks = []
for i in range(int(stock_count)):
    stocks.append(input_stocks(stock_count))
for each_stock in stocks:
    csv_name = each_stock + ".csv"
    stock_statement = "The selected stock is "+ str(each_stock)
    exe_time = "Run at " + str(datetime.today().strftime("%I:%M %p")) + " on " + str(datetime.today().strftime("%B %d, %Y"))
    stock_list = []
    for k, v in stock_dict(each_stock).items():
        if k == "Meta Data":
            information = v["1. Information"]
            ticker = v["2. Symbol"]
            date = datetime.strptime(v["3. Last Refreshed"], "%Y-%m-%d")
            date_statement = "The last refreshed date is " + str(date.strftime("%B %d, %Y"))
            outputsize = v["4. Output Size"]
            timezone = v["5. Time Zone"]
        elif k == "Time Series (Daily)":
            stock_details = v
            for keys, values in stock_details.items():
                stock_date = datetime.strptime(keys, "%Y-%m-%d")
                stock_open = float(values["1. open"])
                stock_high = float(values["2. high"])
                stock_low = float(values["3. low"])
                stock_close = float(values["4. close"])
                stock_volume = int(values["5. volume"])
                stock_info = {"timestamp": date, "open": stock_open, "high": stock_high, "low" :stock_low, "close": stock_close, "volume": stock_volume}
                stock_list.append(stock_info)
                if stock_date == date:
                    latest_price_usd = stock_close
                    latest_price_statement = "The latest closing price is $" + str(latest_price_usd)

    write_csv(csv_name,stock_list)
    print(line)
    print(stock_statement)
    print(exe_time)
    print(date_statement)
    print(latest_price_statement)
    
    all_close = [float(i["close"]) for i in stock_list]
    all_high = [float(i["high"]) for i in stock_list]
    all_low = [float(i["low"]) for i in stock_list]
    print("The average close of the last "+ str(len(all_close)) + " days is "+ str('${0:.2f}'.format(sum(all_close)/len(all_close))))
    print("The average high of the last "+ str(len(all_high)) + " days is "+ str('${0:.2f}'.format(sum(all_high)/len(all_high))))
    print("The average low of the last "+ str(len(all_low)) + " days is "+ str('${0:.2f}'.format(sum(all_low)/len(all_low))))

    #Recommendation
    if latest_price_usd > sum(all_close)/len(all_close)*0.9 and latest_price_usd < sum(all_close)/len(all_close)*1.1:
        print("Recommend holding this stock because it is within 10% of " + str(len(all_close)) + " days moving average")
    elif latest_price_usd > sum(all_close)/len(all_close):
        print("Recommend buying this stock because it is above " + str(len(all_close)) + " days moving average")
    elif latest_price_usd < sum(all_close)/len(all_close):
        print("Recommend selling this stock because it is above " + str(len(all_close)) + " days moving average")






#latest_price_usd = "$100,000.00" # TODO: traverse the nested response data structure to find the latest closing price

#print(f"LATEST DAILY CLOSING PRICE FOR {symbol} IS: {latest_price_usd}")
