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
    clears the terminal
    """
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


# function that does all the scraping
def find_price(soup, ticker, type):
    # searches for the specific tag containing key price information
    results = soup.find("div", class_="intraday__data")
    main_line = results.find_all("bg-quote")
    # print(main_line)

    # refining and stripping down the contents to the number values
    price_info[ticker] = {}

    # add open or closed market status to info section
    if type == "stock":
        try:
            open_or_aftermarket = soup.find("div", class_="element element--intraday")
            status = open_or_aftermarket.find("div")
            price_info[ticker]["Status"] = status.text.strip()
        except AttributeError:
            open_or_aftermarket = soup.find("div", class_="element element--intraday")
            status = open_or_aftermarket.find("div")
            price_info[ticker]["Status"] = status.text.strip()

    price_info[ticker]["Time of Info"] = datetime.now().time().replace(microsecond=0)
    price_info[ticker]["Current Price"] = "$" + main_line[0].text.strip()
    price_info[ticker]["Change ($)"] = main_line[2].text.strip()
    price_info[ticker]["Change (%)"] = main_line[3].text.strip()


# helper function that creates a dynamic link for scraping
def process_link(ticker):
    # link creation
    random_num = random.randint(0,100000)
    link = ""

    link = f"https://www.marketwatch.com/investing/stock/{ticker}?mod=search_symbol/?9082" \
            f"?{random_num}"

    link_txt = urllib.parse.quote(link, safe="%:/?=&*+")
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
        print("\nStock:", key.upper())
        for info in value:
            print(info + ':', value[info])


# helper function that prints out info in a clear and readable way
def display_stock_list(item):
    i = 1
    for key in item:
        print(f"{i}. {key.upper()}")
        i += 1


# allows the user to refresh the entire list in their viewing
def refresh(item, type):
    for stock in item:
        find_price(process_link(stock), stock, type)


# menu that asks for user input to continue, end, or other options
def menu_options(type):
    option = ""
    while True:
        choice = input(f"\n-- Menu --\n1. continue/add item\n2. remove an item\n"
                       f"3. refresh current list\n4. end program\nChoice: ")
        clear()
        if choice in OPTIONS_NUM:
            option = choice
            break
        else:
            print("Invalid Response, please try again")

    if option == "4":  # end program
        return "break"

    elif option == "2":  # removing an item
        clear()
        display_stock_list(price_info)
        remove_stock = input("Item to remove (enter ticker):  ")
        price_info.pop(remove_stock)
        clear()
        display_stock_list(price_info)
        print()

    elif option == "1":  # continue
        clear()
        print("Current Watch List: ")
        display_stock_list(price_info)
        print()
        return "continue"

    elif option == "3":  # refresh
        refresh(price_info, type)
        display_price_info(price_info)
        print()


# main function that deals with user input and interactions
# calls the helper functions to conduct scraping and displaying
def client():
    while True:
        type = ""
        while True:
            type = input("Cryptpocurrency or stock? Or enter stop to end program - ").lower()
            if type == "stock" or type == "crypto" or type == "cryptocurrency":
                break
            elif type == "stop":
                return print("Program Ended")
            else:
                continue

        ticker = input("Enter Symbol/Ticker (ex: AMZN) - ").lower()
        clear()

        if ticker == "stop":
            break

        try:
            # initiates scraping
            soup = process_link(ticker)
            find_price(soup, ticker, type)
            display_price_info(price_info)
        except AttributeError:  # incase the ticker does not exist
            print("Invalid Ticker: item does not exist\nPlease Try Again")

        execute_option = menu_options(type)
        if execute_option == "break":
            break
        elif execute_option == "continue":
            continue


    clear()
    print("Program Ended")


clear()
client()
