#SO HERE IS MY WORK

#INSTALLATIONS 

#If you are working Locally using anaconda, uncomment this lines 
#!pip install yfinance==0.2.38
#!pip install pandas==2.2.2
#!pip install nbformat

!pip install yfinance
!pip install bs4
!pip install nbformat

#importing
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Define Graphing Function
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Question 1: Use yfinance to Extract Stock Data

ticker = yf.Ticker("TSLA")
# Fetch historical market data
historical_data = ticker.history(period="1y")  
# Fetch financials
financials = ticker.financials

# Fetch stock info (e.g., company details, market cap, etc.)
info = ticker.info

#Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data. Set the period parameter to "max" so we get information for the maximum amount of time.
tesla_data = ticker.history(period="max")
print(tesla_data.head())

#Reset the index using the reset_index(inplace=True) function 
tesla_data.reset_index(inplace=True)
print(tesla_data.head())

#Question 2: Use Webscraping to Extract Tesla Revenue Data
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
response = requests.get(url)
html_data = response.text

#Parse the html data using beautiful_soup using parser i.e html5lib or html.parser. Make sure to use the html_data with the content parameter as follow html_data.content .
soup = BeautifulSoup(html_data, 'html5lib')

#Using BeautifulSoup or the read_html function extract the table with Tesla Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue.
tables = pd.read_html(url)
tesla_revenue = tables[1]
tesla_revenue.columns = ['Date', 'Revenue']
print(tesla_revenue.head())

#Execute the following line to remove the comma and dollar sign from the Revenue column.
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)

#Execute the following lines to remove an null or empty strings in the Revenue column
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

#Display the last 5 row of the tesla_revenue dataframe using the tail function. Take a screenshot of the results.
print(tesla_revenue.tail())

#Question 3: Use yfinance to Extract Stock Data

#Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is GME.
gme_ticker = yf.Ticker("GME")

#Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data. Set the period parameter to "max" so we get information for the maximum amount of time.
gme_data = gme_ticker.history(period="max")

#Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.
gme_data.reset_index(inplace=True)

#Question 4: Use Webscraping to Extract GME Revenue Data

#url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
response = requests.get(url)
html_data_2 = response.text

#Parse the html data using beautiful_soup using parser i.e html5lib or html.parser.
soup = BeautifulSoup(html_data_2, 'html.parser')

#Using BeautifulSoup or the read_html function extract the table with GameStop Revenue and store it into a dataframe named gme_revenue. The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column.
tables = pd.read_html(url)
gme_revenue = tables[0]
gme_revenue.columns = ['Date', 'Revenue']
gme_revenue['Revenue'] = gme_revenue['Revenue'].replace({'\$': '', ',': ''}, regex=True).astype(float)

#Display the last five rows of the gme_revenue dataframe using the tail function. Take a screenshot of the results.
print(gme_revenue.tail())

#Question 5: Plot Tesla Stock Graph
#Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph. Note the graph will only show data upto June 2021.

def make_graph(stock_data, revenue_data, title):
    # Ensure the stock_data is limited to data up to June 2021
    stock_data = stock_data[stock_data.index <= '2021-06-30']
    
    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot the stock data
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price', color='tab:blue')
    ax1.plot(stock_data.index, stock_data['Close'], color='tab:blue', label='Stock Price')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a second y-axis for the revenue data
    ax2 = ax1.twinx()
    ax2.set_ylabel('Revenue', color='tab:orange')
    ax2.plot(revenue_data['Date'], revenue_data['Revenue'], color='tab:orange', label='Revenue', linestyle='--')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Add a title and show the plot
    plt.title(title + ' Stock and Revenue Data')
    plt.tight_layout()
    plt.show()

#Question 6: Plot GameStop Stock Graph
#Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the make_graph function is make_graph(gme_data, gme_revenue, 'GameStop'). Note the graph will only show data upto June 2021.
def make_graph(stock_data, revenue_data, title):
    # Ensure the stock_data is limited to data up to June 2021
    stock_data = stock_data[stock_data.index <= '2021-06-30']
    
    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot the stock data
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price', color='tab:blue')
    ax1.plot(stock_data.index, stock_data['Close'], color='tab:blue', label='Stock Price')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a second y-axis for the revenue data
    ax2 = ax1.twinx()
    ax2.set_ylabel('Revenue', color='tab:orange')
    ax2.plot(revenue_data['Date'], revenue_data['Revenue'], color='tab:orange', label='Revenue', linestyle='--')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Add a title and show the plot
    plt.title(title + ' Stock and Revenue Data')
    plt.tight_layout()
    plt.show()

