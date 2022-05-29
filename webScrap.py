# created by: Tsz Kit Wong
# webScrap.py

from bs4 import BeautifulSoup
from datetime import date
import requests
import urllib.parse

# creating url based on user input
ticker = input("Enter Stock Symbol/Ticker (ex: AMZN) - ").upper()
link = f"https://finance.yahoo.com/quote/{ticker}/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&" \
       f"guce_referrer_sig=AQAAACUcyFsclu9rOyzDodJC1Cv2K0DOU0G4woBHTbUAxV0b0YnYVx35_g2_Kkh8C61IA4nySLZno0UVelD" \
       f"GvH57SGrTu5mXnkE5RbBN0xD-UxYOk-mKWiLJKR54HPtQXhL8QkOajVH3FxowIaW2lYPwJNSqkP9lvY7tDqeTA7ujnvu0"

# link creation, requestion, and parse
link_txt = urllib.parse.quote(link, safe="%:/?=&*+")
page = requests.get(link_txt)
soup = BeautifulSoup(page.content, "html.parser")

# searching in results for desired info
results = soup.find("div", class_="D(ib) Mend(20px)")
main_line = results.find_all("fin-streamer")
price_info = {}
for i in range(0,len(main_line)):
       if i == 0:
              price_info["curr_price"] = "$" + main_line[i].text.strip()
       if i == 1:
              price_info["daily_inc"] = main_line[i].text.strip()
       if i == 2:
              price_info["daily_per_inc"] = main_line[i].text.strip()

# if market is closed, will display after market price as well
curr_datetime = datetime.now(timezone.utc).hour
if curr_datetime > 20:

print(price_info)
