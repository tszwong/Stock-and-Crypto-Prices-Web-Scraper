# created by: Tsz Kit Wong
# webScrap.py

from bs4 import BeautifulSoup
from datetime import datetime, date, timezone
import requests
import urllib.parse


# storing the stocks
price_info = {}


def find_price(soup, ticker):
       """ searches for the price info based on link and adds
           it to the dict price_info for storage
       """
       
       # searching in results for desired info
       results = soup.find("div", class_="D(ib) Mend(20px)")
       main_line = results.find_all("fin-streamer")
       
       price_info[ticker] = {}
       price_info[ticker]["curr_price"] = "$" + main_line[0].text.strip()
       price_info[ticker]["daily_change"] = main_line[1].text.strip()
       price_info[ticker]["daily_pct_change"] = main_line[2].text.strip('()')


def process_link(ticker):
       """ creates a link based on user input 
           which will be used for web scraping
       """
       
       # creating url based on user input
       link = f"https://finance.yahoo.com/quote/{ticker}/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29v" \
           f"Z2xlLmNvbS8&guce_referrer_sig=AQAAACUcyFsclu9rOyzDodJC1Cv2K0DOU0G4woBHTbUAxV0b0YnYVx35_g2_Kk" \
           f"h8C61IA4nySLZno0UVelDGvH57SGrTu5mXnkE5RbBN0xD-UxYOk-mKWiLJKR54HPtQXhL8QkOajVH3FxowIaW2lYPwJNSq" \
           f"kP9lvY7tDqeTA7ujnvu0"

       # link creation, requestion, and parse
       link_txt = urllib.parse.quote(link, safe="%:/?=&*+")
       page = requests.get(link_txt)
       soup = BeautifulSoup(page.content, "html.parser")
       
       return soup


# if market is closed, will display after market price as well
curr_datetime = datetime.now(timezone.utc).hour
if curr_datetime > 20:
       after_market_results = soup.find("div", class_="Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)").\
              find_all("fin-streamer")
       price_info[ticker]["after_market_price"] = "$" + after_market_results[1].text.strip()
       price_info[ticker]["after_market_change"] = after_market_results[2].text.strip()
       price_info[ticker]["after_market_pct_change"] = after_market_results[3].text.strip('()')

       
ticker = input("Enter Stock Symbol/Ticker (ex: AMZN) - ").upper()
print(price_info)
