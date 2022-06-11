# created by: Tsz Kit Wong
# webScrap.py

from bs4 import BeautifulSoup
from os import system, name
from datetime import datetime, date, timezone
import requests
import urllib.parse
import sys


# info that will be displayed to user
price_info = {}
stocks_list = []
curr_time = f"{datetime.now().month}/{datetime.now().day}/{datetime.now().year} " \
            f"{datetime.now().time().replace(microsecond=0)}"


def clear():
    """
    clears the commandline
    """
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


# function that does all the web scraping
def find_price(soup, ticker):
    # searches for the specific tag containing key price information
    results = soup.find("div", class_="D(ib) Mend(20px)")
    main_line = results.find_all("fin-streamer")

    # refining and stripping down the contents to the number values 
    price_info[ticker]["Current Price"] = "$" + main_line[0].text.strip()
    price_info[ticker]["Daily Change"] = main_line[1].text.strip()
    price_info[ticker]["Daily Change %"] = main_line[2].text.strip('()')
    stocks_list.append(ticker)  # adding the stock we searched to the list

#     after_market_results = soup.find("div", class_="Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)"). \
#         find_all("fin-streamer")
#     price_info[ticker]["Current After Market Price"] = "$" + after_market_results[1].text.strip()
#     price_info[ticker]["After Market Change"] = after_market_results[2].text.strip()
#     price_info[ticker]["After Markey Change in %"] = after_market_results[3].text.strip('()')


# helper function that creates a dynamic link for scraping
def process_link(ticker):
    
    # link creation
    link = f"https://finance.yahoo.com/quote/{ticker}/"
    link_txt = urllib.parse.quote(link, safe="%:/?=&*+")

    # getting the html file contents
    page = requests.get(link_txt)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup


# helper function that prints out info in a clear and readable way
def display(item):
    if type(item) == dict:
        for key, value in price_info.items():
            print("\nStock:", key)
            for info in value:
                print(info + ':', value[info])
    else:
        for i in range(1, len(item)+1):
            print(i, item[i-1])
    print()


# main function that deals with user input and interactions
# calls the helper function to conduct scraping
def client():
    while True:
        ticker = input("Enter Stock Symbol/Ticker (ex: AMZN) - ").upper()
        clear()
        if ticker == "stop".upper():
            break
        
        try:
            # initiates scraping
            soup = process_link(ticker)
            find_price(soup, ticker)
            print(f"Prices as of {curr_time}")
            display(price_info)
            
        except AttributeError:  # incase the ticker does not exist
            print("Invalid Ticker: stock does not exist\nPlease Try Again")

        options_num = "123"
        option = ""
        while True:
            choice = input(f"\n-- Menu --\n1. continue/add stock\n2. remove a stock\n"
                           f"3. stop\nChoice: ")
            clear()
            if choice in options_num:
                option = choice
                break
            else:
                print("Invalid Response, please try again")

        if option == "3":  # end program
            break
            
        elif option == "2":
            clear()
            print(stocks_list)
            remove_stock = input("Stock to remove:  ")
            price_info.pop(remove_stock)
            stocks_list.remove(remove_stock)
            clear()
            print("Price Info:\n")
            display(price_info)
            
        elif option == "1":
            clear()
            print("Current Watch List: ")
            display(stocks_list)
            continue

    clear()
    print("Program Ended")


client()
