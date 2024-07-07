
import requests
from bs4 import BeautifulSoup 
from random import randrange,uniform
from lxml import etree 
from datetime import date as d 
from datetime import datetime
import json 
import os 
import pytz
from time import sleep
from multiprocessing import Process

global tz_NY
tz_NY = pytz.timezone('America/New_York') 
global stop_flag
stop_flag = True
class company_data_price:
      def __init__(self, stock):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        self.base_url = f'https://finance.yahoo.com/quote/{stock}/'
        self.dom = self.fetch_data(self.base_url)
        self.stock = stock
        #self.base_source = self.dom.xpath(f"//[@data-symbol={str(stock)}]")

      def fetch_data(self,url:str):
          try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")
            return etree.HTML(str(soup))
          except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

      def store_data(self):
          price_dict = {"price": float(self.find_data("regularMarketPrice")),"date":str(d.today()),"company":str(self.stock),"Time_machine":str(datetime.now().strftime("%H:%M:%S")),"time_nasdaq":str(datetime.now(tz_NY).strftime("%H:%M:%S"))}
          if os.path.exists("Stored_data.json"):
            with open("Stored_data.json", "r") as infile:
                try:
                    self.existing_data = json.load(infile)
                except (FileNotFoundError,json.JSONDecodeError):
                    self.existing_data = []
          else:
              self.existing_data = []
          self.existing_data.append(price_dict)
          with open("Stored_data.json","w") as outfile:
              json.dump(self.existing_data, outfile, indent=4)
         

      def find_data(self,field):
          if self.dom is None:
              return "[!] Data fetch Error"
          list_of_elements =  self.dom.xpath(f"//*[@data-field='{field}']")
          for element in list_of_elements:
             data_value = element.get('data-value')
             return(data_value)
          
                     
      def find_stock_price(self):
          #self.store_data()
          return self.find_data("regularMarketPrice") 
           
      def find_previous_close(self):
          return self.find_data("regularMarketPreviousClose")
      def find_open(self):
         return self.find_data("regularMarketOpen")
      def find_marketcap(self):
         return self.find_data("marketCap")
      def find_avg_volume(self):
         return self.find_data("averageVolume")
      def find_est(self):
          return self.find_data("targetMeanPrice")
      def find_eps(self):
          return self.find_data("trailingPE")
    
      
      
class company_financials:
    def __init__(self,stock):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        self.base_url = f'https://finance.yahoo.com/quote/{stock}/key-statistics/'
        self.base_html = requests.get(self.base_url,headers=self.headers)
        #self.base_data = self.base_html.text
        #self.base_source = self.soup.find_all("td",{'class':"value svelte-vaowmx"})
        self.soup = BeautifulSoup(self.base_html.content, "lxml")
        self.dom = etree.HTML(str(self.soup))
        self.stock = stock
        self.base_source = self.dom.xpath("//*[@class='value svelte-vaowmx']")
    def find_beta(self):
        return self.base_source[22].text
    def find_fiscal_year_end(self):
        return self.base_source[0].text
    def recent_quarter(self):
        return self.base_source[1].text
    def profit_margin(self):
        return self.base_source[2].text
    def operating_margin(self):
        return self.base_source[3].text
    def revenue(self):
        return self.base_source[6].text
    def revenue_per_share(self):
        return self.base_source[7].text
    def year_high(self):
        return self.base_source[25].text
    def year_low(self):
        return self.base_source[26].text
    def fifty_ema(self):
        return self.base_source[27].text
    def twohundred_ema(self):
        return self.base_source[28].text

class company_check:
    def __init__(self,stock):
        
        self.fifty_ema = company_financials(stock).fifty_ema()
        self.price = company_data_price(stock).find_stock_price()
        self.twohundredema = company_financials(stock).twohundred_ema()

    def ema_check_fifty(self):
        if self.fifty_ema > self.price:
            return "[[!]Price is lower than 50EMA...]"
        elif self.fifty_ema < self.price:
            return "[[!]Price is higher than 50EMA...]"
        else:
            "[[!]Price is equal to 50EMA...]"
    
    def ema_check_twohundred(self):
         if self.twohundredema > self.price:
            return "[[!]Price is lower than 200EMA...]"
         elif self.twohundredema < self.price:
            return "[[!]Price is higher than 200EMA...]"
         else:
            "[[!]Price is equal to 200EMA...]"
    
    def get_last_checked_price(self):
        with open ("Stored_data.json", "r") as file : 
           self.data = json.load(file)
           return self.data[-1]["price"]
        
       
    
#TODO upgrade the update code and import threading to do code 
class online_data:
    def __init__(self,stock):
        self.financials = company_financials(stock)
        self.data = company_data_price(stock)
        self.check = company_check(stock)
        self.data.find_stock_price()

    def convert_type(self,variable):
        self.value_float = float(variable.replace(",", ""))
        return self.value_float

            
    def check_yearly_high(self):
        if self.check.get_last_checked_price()> self.convert_type(self.financials.year_high()):
            return "[!!! New yearly High]"
        else:
            print("No yearly high!!")
    def check_yearly_low(self):
        if self.check.get_last_checked_price() < self.convert_type(self.financials.year_low()):
            return "[!!! New yearly low...]"
        else:
            print("No yearly low!! ")
    



    
    


            
                




