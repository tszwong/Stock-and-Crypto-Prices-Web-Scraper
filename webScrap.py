# created by: Tsz Kit Wong
# webScrap.py

from bs4 import BeautifulSoup
from datetime import date
import requests
import urllib.parse


ticker = input("Enter Stock Symbol/Ticker (ex: AMZN) - ").upper()
link = f"https://finance.yahoo.com/quote/{ticker}/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&" \
       f"guce_referrer_sig=AQAAACUcyFsclu9rOyzDodJC1Cv2K0DOU0G4woBHTbUAxV0b0YnYVx35_g2_Kkh8C61IA4nySLZno0UVelD" \
       f"GvH57SGrTu5mXnkE5RbBN0xD-UxYOk-mKWiLJKR54HPtQXhL8QkOajVH3FxowIaW2lYPwJNSqkP9lvY7tDqeTA7ujnvu0"

link_txt = urllib.parse.quote(link, safe="%:/?=&*+")
page = requests.get(link_txt)
soup = BeautifulSoup(page.content, "html.parser")
print(link_txt)
