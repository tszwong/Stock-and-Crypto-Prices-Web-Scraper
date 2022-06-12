# created by: Tsz Kit Wong
# webScrap.py

from bs4 import BeautifulSoup
from os import system, name
from datetime import datetime, date, timezone
import requests
import urllib.parse
import sys
import random


# constants
OPTIONS_NUM = "1234"

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
    results = soup.find("div", class_="intraday__data")
    main_line = results.find_all("bg-quote")
    # print(main_line)

    # refining and stripping down the contents to the number values
    price_info[ticker] = {}
    price_info[ticker]["Time of Info"] = datetime.now().time().replace(microsecond=0)
    price_info[ticker]["Current Price"] = "$" + main_line[0].text.strip()
    price_info[ticker]["Daily Change ($)"] = main_line[2].text.strip()
    price_info[ticker]["Daily Change (%)"] = main_line[3].text.strip()
    stocks_list.append(ticker)  # adding the stock we searched to the list

    # try:
    #     after_market_results = soup.find("div", class_="Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)"). \
    #         find_all("fin-streamer")
    #     price_info[ticker]["After Market Price"] = "$" + after_market_results[1].text.strip()
    #     price_info[ticker]["After Market Change"] = after_market_results[2].text.strip()
    #     price_info[ticker]["After Market Change %"] = after_market_results[3].text.strip('()')
    #
    # except AttributeError:
    #     print("No after market price currently")


# helper function that creates a dynamic link for scraping
def process_link(ticker):
    # link creation
    random_num = random.randint(0,100000)
    link = ""
    if type == "stock":
        link = f"https://www.marketwatch.com/investing/stock/{ticker}?mod=search_symbol/?9082" \
               f"?{random_num}"
    elif type == "cryptocurrency" or type == "crypto":
        link = f"https://www.marketwatch.com/investing/cryptocurrency/{ticker}?{random_num}"
    # print(link_txt)

    # getting the html file contents
    page = requests.get(link_txt)
    # print(page.content)
    soup = BeautifulSoup(page.content, "html.parser")
    page.close()
    return soup


# helper function that prints out info in a clear and readable way
def display_price_info(item):
    for key, value in item.items():
        print("\nStock:", key)
        for info in value:
            print(info + ':', value[info])


# helper function that prints out info in a clear and readable way
def display_stock_list(item):
    i = 1
    for key in item:
        print(f"{i}. {key}")
        i += 1


def refresh(item):
    for stock in item:
        find_price(process_link(stock), stock)


# main function that deals with user input and interactions
# calls the helper function to conduct scraping
def client():
    while True:
        type = input("Crpytpocurrency or stock?\nEnter stop to end program - ").lower()
        ticker = input("Enter Stock Symbol/Ticker or Stop (ex: AMZN) - ").lower()
        clear()

        if type == "stop":
            break

        try:
            # initiates scraping
            soup = process_link(ticker)
            find_price(soup, ticker)
            display_price_info(price_info)

        except AttributeError:  # incase the ticker does not exist
            print("Invalid Ticker: stock/crypto does not exist\nPlease Try Again")

        option = ""
        while True:
            choice = input(f"\n-- Menu --\n1. continue/add item\n2. remove an item\n"
                           f"3. end program\n4. refresh current list\nChoice: ")
            clear()
            if choice in OPTIONS_NUM:
                option = choice
                break
            else:
                print("Invalid Response, please try again")

        if option == "3":  # end program
            break

        elif option == "2":
            clear()
            display_stock_list(price_info)
            remove_stock = int(input("Item to remove(enter index) :  "))
            price_info.pop(stocks_list[remove_stock-1])
            clear()
            display_price_info(price_info)

        elif option == "1":
            clear()
            print("Current Watch List: ")
            display_stock_list(price_info)
            continue

        elif option == "4":
            refresh(price_info)
            display_price_info(price_info)
            print()

    clear()
    print("Program Ended")


clear()
client()
