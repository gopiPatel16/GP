#installations code
!pip install pandas
!pip install requests
!pip install bs4
!pip install html5lib
!pip install lxml
!pip install plotly

#importing pandas and requests 
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Extracting the data from webpage(Netflix data)

#sending HTTP request
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
data  = requests.get(url).text #requests.get() method takes a URL as its first argument, which specifies the location of the resource to be retrieved.
print(data)

#Parsing data(process of analyzing a string of data)
soup = BeautifulSoup(data, 'html.parser') #creating object of BeautifulSoup and passing 2 arguments 

 #After scrapping content of web page,converting the table into a data frame.
netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])

#After converting into table,we will use methods like find() to extract data
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    
    # Finally we append the data of each row to the table
    netflix_data = pd.concat([netflix_data,pd.DataFrame({"Date":[date], "Open":[Open], "High":[high], "Low":[low], "Close":[close], "Adj Close":[adj_close], "Volume":[volume]})], ignore_index=True)    
netflix_data.head()#print the data
