import requests
from datetime import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
SID ="AC14792dea4010fe41059bdff9e7cafe72"
AUTHTOK = "18d41206c13fb8426bd61830b0d57968"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
dt = datetime.now()
day = dt.day

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two
# prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 

stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": "OK7Z1SU9AHWPZ0S0",
    "slice": "year1month1"
}
stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()
yesterday_closing = float(stock_data["Time Series (60min)"][f"2023-03-0{day - 1} 20:00:00"]["4. close"]) #100
day_before_yesterday_closing = float(stock_data["Time Series (60min)"][f"2023-03-0{day - 2} 20:00:00"]["4. close"]) #60
print(yesterday_closing)
print(day_before_yesterday_closing)

if yesterday_closing > day_before_yesterday_closing:
    change = yesterday_closing - day_before_yesterday_closing
    symbol = "🔺"
else:
    change = day_before_yesterday_closing - yesterday_closing
    symbol = "🔻"

if change > (yesterday_closing * 0.05):
## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator

    news_params = {
        "q": COMPANY_NAME,
        "apiKey": "e2d49875773f45cfb17778d367c23eca"
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    news_data = news_data[0:3]
    print(news_data)
## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.
    percentage_change = round((change / yesterday_closing) * 100, 2)
    client = Client(SID, AUTHTOK)
    message = client.messages \
                    .create(
                         body=f"TSLA: {symbol}{percentage_change}%\n\nHeadline: {news_data[0]['title']}\n\n"
                              f"Brief: {news_data[0]['content']}",
                         from_='+15075288344',
                         to='+26777808353'
                     )

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
"""

