import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import re
from bs4 import BeautifulSoup
import html5lib
import datetime as dt


url = "https://finance.yahoo.com/quote/SPY/options"

driver = webdriver.Chrome('/Users/patrik/Downloads/chromedriver') #locates web driver in downloads directory

driver.get(url) # fetches the url on which we want to run our scraper

driver.find_element_by_xpath("//button[@value='agree']").click() # clicks through all the bs terms and conditions

time.sleep(20)

try:
    driver.find_element_by_xpath('//button[@class="Mx(a) Fz(16px) Fw(600) Mt(20px) D(n)--mobp"]').click()
except:
    pass


class Option_Chains():
    def __init__(self, Stock):
        self.Call_Dataframe = None
        self.Put_Dataframe = None
        self.Expiry = driver.find_element_by_xpath('//span[@class="Fz(s) Mend(10px)"][2]').text
        self.Ticker = Stock
        self.Spot_Price = float(driver.find_element_by_xpath('//fin-streamer[@class="Fw(b) Fz(36px) Mb(-4px) D(ib)"]').text)

    def Call_Option_Dataframe(self):

        webpage = driver.page_source

        soup = BeautifulSoup(webpage, 'html.parser')

        tables = soup.find_all('table')

        table = soup.find('table', class_="calls W(100%) Pos(r) Bd(0) Pt(0) list-options")  # find calls table

        df = pd.DataFrame(columns=['Price of Option', 'Strike of Option', 'Spot of Stock', 'Time Until Expiry'])

        for i in table.tbody.find_all('tr'):  # table row
            # Find all data for each column
            columns = i.find_all('td')  # table data on all the columns

            if columns != []:
                price = columns[3].text.strip()
                strike = columns[2].text.strip()

            df2 = pd.DataFrame({'Price of Option': [price], 'Strike of Option': [strike],
                                'Spot of Stock' : [self.Spot_Price], 'Time Until Expiry': [(dt.datetime.strptime(
                                self.Expiry, '%B %d,  %Y').date() - dt.date.today()).days]})

            df = pd.concat([df, df2], ignore_index=True)

        self.Call_Dataframe = df

    """def Put_Option_Dataframe(self):

        webpage = driver.page_source

        soup = BeautifulSoup(webpage, 'html.parser')

        tables = soup.find_all('table')

        table = soup.find()  # find puts table

        df = pd.DataFrame(columns=['Price of Option', 'Strike of Option'])

        for i in table.tbody.find_all('tr'):  # table row
            # Find all data for each column
            columns = i.find_all('td')  # table data on all the columns

            if columns != []:
                price = columns[3].text.strip()
                strike = columns[2].text.strip()

            df2 = pd.DataFrame({'Price of Option': [price], 'Strike of Option': [strike]})
            df = pd.concat([df, df2], ignore_index=True)

        self.Put_Dataframe = df""" #Put Options

expiry_dates = Select(driver.find_element_by_xpath('//select[@class="Fz(s) H(25px) Bd Bdc($seperatorColor)"]'))
# goes into the selector to choose all the expiry dates

calls_dict = {}
puts_dict = {}

for index in range(len(expiry_dates.options)):
    # iterates through all the selections in the drop-down of different expires

    expiry_dates = Select(driver.find_element_by_xpath(
        '//select[@class="Fz(s) H(25px) Bd Bdc($seperatorColor)"]'))
    # goes into the selector to choose all the expiry dates
    expiry_dates.select_by_index(index)   # clicks on every selection

    time.sleep(2)

    calls_dict[driver.find_element_by_xpath('//span[@class="Fz(s) Mend(10px)"][2]').text] = \
        Option_Chains("SPY")
    calls_dict[driver.find_element_by_xpath('//span[@class="Fz(s) Mend(10px)"][2]').text].Call_Option_Dataframe()

large_call_data_frame = pd.concat([i.Call_Dataframe for i in calls_dict.values()], ignore_index = True)

large_call_data_frame.to_csv(f'/Users/patrik/Desktop/Options Data/Calls_Dataframe_{dt.date.today()}.csv')



#my_list = re.split('\n', driver.find_element_by_xpath('//select[@class="Fz(s) H(25px) Bd Bdc($seperatorColor)"]').text) # expiry dates for options




