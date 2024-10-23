import requests
from bs4 import BeautifulSoup
site = "http://www.time.ir/"
response = requests.get(site)   
soup = BeautifulSoup(response.content , "html.parser")
div_tage = soup.find_all("div" , {"class": "randomQuote"} )
for tage in div_tage:
    pTag =  tage.find_all("span")
    for tage in pTag:
        print(tage.text)

