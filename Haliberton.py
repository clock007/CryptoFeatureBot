import requests
from datetime import datetime
from time import time
import pandas as pd
import matplotlib.pyplot as plt
import time as s
from time import sleep
from datetime import datetime
from time import time
import pandas as pd
import matplotlib.pyplot as plt
from threading import Thread
from time import sleep
from coinexpy.coinex import Coinex
import numpy as np
import json
from lib import CoinexPerpetualApi
import requests
from datetime import datetime
from time import time
import pandas as pd
import matplotlib.pyplot as plt
import time as s
from threading import Thread




 
base_url = "https://api.kucoin.com"


access_id='DE6FC0BC839F46CA9C01DC97A16FF6BA'
secret_key='86E84A6C5CB0423BB35FFCB738E39065EA9A330078CF6A50'
    



Robot = CoinexPerpetualApi(access_id, secret_key)

coin_pair = "BTC-USDT" #BTC-USDT
frequency = "4hour" #1hour 4hour 1min
F_Market='BTCUSDT'
Margin=10
Limit=50
F_amount=0.001
Sood_Unit=0.01

#get timestamp date of today in seconds


#----------------------------------------
Current_Type=""
Sell_Counter=0
Buy_Counter=0
Sell_Price=0
Buy_Price=0

Active_Order=0
Count_of_Order=5
#-------------------------------------------
F_Result=Robot.adjust_leverage(F_Market,1,5)
F_Result=Robot.adjust_leverage(F_Market,2,5)
print("Leverage Status:")
print(F_Result)
print("Buy Result:")
Robot.put_limit_order
print('Market State')
Temp=Robot.get_market_state('BTCUSDT')
print(Temp)
Current_Price=float(Temp['data']['ticker']['last'])


while True:
    now_is = int(time())
    days = 12
               #sec  min  hour days
    days_delta = 60 * 60 * 24 * days
    start_At = now_is - days_delta
    #print(now_is)
    price_url = f"/api/v1/market/candles?type={frequency}&symbol={coin_pair}&startAt={start_At}&endAt={now_is}"

    price_dict = {}
    #Position=""
    try:
        print('Market State')
        Temp=Robot.get_market_state('BTCUSDT')
        #print(Temp)
        
        prices = requests.get(base_url+price_url).json()
        for item in prices['data']:
            #convert date from timestamp to Y M D
            date_converted = datetime.fromtimestamp(int(item[0])).strftime("%Y-%m-%d, %H:%M:%S")
            price_dict[date_converted] = item[2]
            
    
        priceDF = pd.DataFrame(price_dict,index=["price"]).T
        #Convert prices into a float
        priceDF['price'] = priceDF['price'].astype(float)
            
        #convert dates to datetime from object
        priceDF.index = pd.to_datetime(priceDF.index)
        
        #reverse dates
        priceDF = priceDF.iloc[::-1]
        #print(priceDF)

    except:
        continue
        pass
   
    for i in range(0,1):
        try:
         
            Current_Price=float(Temp['data']['ticker']['last'])
            limit=0.0005*(Current_Price)
            #F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Current_Price-60)
            print("Current price is")
            print(Current_Price)  
            #-------------------------------------------------------------------
    
        # Test      
              
        except:
            continue
            pass
            
    
        priceDF['12MA'] = priceDF['price'].ewm(span=12, adjust=False, min_periods=12).mean()
        priceDF['26MA'] = priceDF['price'].ewm(span=26, adjust=False, min_periods=26).mean()
            
        
        
        


        priceDF['MACD'] = priceDF['12MA']-priceDF['26MA']
        priceDF['MACDS'] = priceDF['MACD'].ewm(span=9, adjust=False, min_periods=9).mean()

        Last_Indices=len(priceDF['MACDS'])
        Last_Indices=Last_Indices-1

             
        Current_MACD=priceDF['MACD'][Last_Indices]
        Current_MACDS=priceDF['MACDS'][Last_Indices]

        Current_MACD_1=priceDF['MACD'][Last_Indices-1]
        Current_MACDS_1=priceDF['MACDS'][Last_Indices-1]

        Current_MACD_2=priceDF['MACD'][Last_Indices-2]
        Current_MACDS_2=priceDF['MACDS'][Last_Indices-2]

        Current_MACD_3=priceDF['MACD'][Last_Indices-3]
        Current_MACDS_3=priceDF['MACDS'][Last_Indices-3]
        
        Delta=float(Current_MACD)-float(Current_MACDS)
        Delta_1=float(Current_MACD_1)-float(Current_MACDS_1)
        Delta_2=float(Current_MACD_2)-float(Current_MACDS_2)
        Delta_3=float(Current_MACD_3)-float(Current_MACDS_3)
        
        print("MACD and MACDS pair")
        print(Current_MACD)
        print(Current_MACDS)

        print(Current_MACD_1)
        print(Current_MACDS_1)

        print(Current_MACD_2)
        print(Current_MACDS_2)

        print(Current_MACD_3)
        print(Current_MACDS_3)

        Limit=float(0.0005*Current_Price)
#-----------------------------------------Check Validity -------------------------------------------------
        if(Delta < 0 and Current_Type=="Buy" and Current_Price>0):
            print("Not Valid Buy")
            try:
                Robot.cancel_all_order(F_Market)
                
                Buy_Counter=0
                sleep(0.5)
                try:
                    F_result=Robot.query_position_pending()
                    print(F_result)
                    print(F_result['code'])
                    for item in F_result['data']:
                        print(item['market'])
                        print(item['position_id'])
                        print(item['side'])
                        print(item['first_price'])
                        print(item['latest_price'])
                        print('-----------')
                        if(str(item['side'])=='2'):
                            print('Buy')
                        if(str(item['market'])==F_Market):
                            print('it is BTC')
                            F_result=Robot.close_market(F_Market,item['position_id'])
                            print(F_result)
                        Current_Type=""
                        Buy_Counter=0
                        Active_Order=0   
                except:
                    print('can not cancell position buy Pending')
                                    
            except:
                print("Failed to cancel Mistake order")


        if(Delta > 0 and Current_Type=="Sell" and Current_Price>0):
            print("Not Valid Sell")
            try:
                Robot.cancel_all_order(F_Market)
                sleep(0.5)
                try:
                    F_result=Robot.query_position_pending()
                    print(F_result)
                    print(F_result['code'])
                    for item in F_result['data']:
                        print(item['market'])
                        print(item['position_id'])
                        print(item['side'])
                        print(item['first_price'])
                        print(item['latest_price'])
                        print('-----------')
                        if(str(item['side'])=='1'):
                            print('SELL')
                        if(str(item['market'])==F_Market):
                            F_result=Robot.close_market(F_Market,item['position_id'])
                            print(F_result)
                        Current_Type=""
                        Sell_Counter=0
                        Active_Order=0
                except:
                    print('can not cancell position')
                    
            except:
                print("Failed to cancel mistake order")
               
        #F_Result=Robot.put_market_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount)
        #print(F_Result['code'])
        #print(F_Result['message'])

        
#-------------------------------------- Check Price ---------------------------------------------
#-----------------------------------------Check Validity (2)----------------------------------------
        if(Delta < 0 and Current_Type=="Buy" and Current_Price>0 and Active_Order <Count_of_Order ):
            print("Not Valid Buy")
            try:
                Robot.cancel_all_order(F_Market)
                
                Buy_Counter=0
                sleep(0.5)
                try:
                    F_result=Robot.query_position_pending()
                    print(F_result)
                    print(F_result['code'])
                    for item in F_result['data']:
                        print(item['market'])
                        print(item['position_id'])
                        print(item['side'])
                        print(item['first_price'])
                        print(item['latest_price'])
                        print('-----------')
                        if(str(item['side'])=='2'):
                            print('Buy')
                        if(str(item['market'])==F_Market):
                            print('it is BTC')
                        F_result=Robot.close_market(F_Market,item['position_id'])
                        print(F_result)
                        Current_Type=""
                        Buy_Counter=0  
                        Active_Order=0
                except:
                    print('can not cancell position')
            except:
                print('Failed Cancell order')                        


        if(Delta > 0 and Current_Type=="Sell" and Current_Price>0 and Active_Order < Count_of_Order):
            print("Not Valid Sell")
            try:
                Robot.cancel_all_order(F_Market)
                sleep(0.5)
                try:
                    F_result=Robot.query_position_pending()
                    print(F_result)
                    print(F_result['code'])
                    for item in F_result['data']:
                        print(item['market'])
                        print(item['position_id'])
                        print(item['side'])
                        print(item['first_price'])
                        print(item['latest_price'])
                        print('-----------')
                        if(str(item['side'])=='1'):
                            print('SELL')
                        if(str(item['market'])==F_Market):
                            F_result=Robot.close_market(F_Market,item['position_id'])
                            print(F_result)
                        Current_Type=""
                        Sell_Counter=0
                        Active_Order=0
                except:
                    print('can not cancell position')
                    
            except:
                print("Failed to cancel mistake order")
            
               
        #F_Result=Robot.put_market_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount)
        #print(F_Result['code'])
        #print(F_Result['message'])

        
#-------------------------------------- Check Price -------------------------------------------------
        print("Begin Checking Price")
        
               
                

        if((Delta > Limit) and (Delta_1 < 0 or Delta_2 <0 or Delta_3 <0)  and Current_Type!="Buy" and Current_Price>0):
            print("----------------------------  Buy Step Satisfied-------------------------------")
            print("Buy Counter")
            print(Buy_Counter)
            Buy_Counter=Buy_Counter+1
            Sell_Counter=0
            if(Buy_Counter > 20):
                try:
                    #Robot.cancel_all_order(F_Market)
                    #sleep(1)
                    #Robot.cancel_all_order(F_Market)
                    #sleep(3)
                    F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount, Current_Price+60)
                    sleep(0.5)
                    Active_Order=Active_Order+1
                    Buy_Price=Current_Price
                    Buy_Counter=0
                   
                    #F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount, Current_Price+300)
                    #sleep(0.5)
                    
                    print("********************** Buy *************************")
                    Buy_Price=Current_Price
                    if(Count_of_Order <= Active_Order):
                        Current_Type="Buy"

                  
                except:
                    print("Failed To Buy")
                    continue
                    pass



#-------------------------------------------------------Sell Part------------------------------------------------------------------        
       

        if((Delta < -1*Limit and (Delta_1 > 0 or Delta_2 >0 or Delta_3>0) ) and Current_Type!="Sell" and Current_Price>0):
            print("----------------------------  Sell Step Satisfied-------------------------------")
            Sell_Counter=Sell_Counter+1
            Buy_Counter=0
            print("Sell Counter")
            print(Sell_Counter)
            if(Sell_Counter > 20):
                try:
                    
                    
                    
                    F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Current_Price-100)
                    sleep(0.5)
                    Active_Order=Active_Order+1
                    Sell_Price=Current_Price
                    Sell_Counter=0
                   
                    #F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Current_Price-300)
                    #sleep(0.5)
                    print("********************** Sell *************************")

                    if(Count_of_Order <= Active_Order):
                        
                        Active_Order=Count_of_Order
                        Current_Type="Sell"
                   
                    
                    
                    
                   
                except:
                    print("Failed To Sell")
                    continue
                    pass
                
        
        #-----------------------------------------Save SOOD -------------------------------------------------
        if(Current_Type=="Buy" ):
            if(Current_Price >0 and ((float(Current_Price)-float(Buy_Price))/float(Buy_Price))>Sood_Unit):
                try:
                    F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Current_Price-130)
                    Buy_Price=Current_Price
                    Active_Order=Active_Order-1

                    
                    
                    
                except:
                    print("Save Soof Failed")
                    continue
                    pass


            
       
                

        if(Current_Type=="Sell" ):
            if(Current_Price >0 and ((float(Sell_Price)-float(Current_Price))/float(Current_Price))>Sood_Unit):
                try:
                    #F_result=Robot.put_market_order(F_Market, Robot.ORDER_DIRECTION_SELL, int(float(F_amount/3)))
                    F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount, Current_Price+130)
                    Sell_Price=Current_Price
                    Active_Order=Active_Order-1
                  
                except:
                    print("Save Soof Failed")
                    continue
                    pass

        
    
            
               
        sleep(10)
                
 

    
