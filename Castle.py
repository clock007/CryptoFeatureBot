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


F_Market_=['MANAUSDT']
print(F_Market_[0])

Limit_=[0.009]
F_amount_=[40]
leverage=[10]
leverage_2=[3]


Buy_Price_Order=[0]
Sell_Price_Order=[0]
Stop_Price_=[2.485,0.8633]
Stop_Bit=44950
Begin_Buy_=[0]
Current_Price=[0]
Zarar=[50]
Stop_Price_Up=0.00000204
Stop_Price_Down=0.00000185


#get timestamp date of today in seconds


#----------------------------------------
Seen=1
#----------------------------------------
i=0
for Begin_Buy,F_Market in zip(Begin_Buy_,F_Market_):
    if(Begin_Buy!=0):
        Robot.put_market_order(market=F_Market, side=2, amount=Begin_Buy)
        sleep(1)

    Temp=Robot.get_market_state(F_Market)
    #print(Temp)
    Current_Price[i]=float(Temp['data']['ticker']['last'])
    

    #print("-------position-------")
    Res=Robot.query_position_pending(market=F_Market)
    #print(Res['data'][0]['type'])
    sleep(1)
    F_Result=Robot.adjust_leverage(F_Market,1,leverage[i])
    F_Result=Robot.adjust_leverage(F_Market,2,leverage[i])
    sleep(1)
    i=i+1

Counter=0
while(True):
    sleep(2)
  
    F_result_Sell="";   F_result_Buy=""

    
    try:
        i=0
        for Begin_Buy, F_Market, Stop_Price, F_amount, Limit in zip(Begin_Buy_, F_Market_, Stop_Price_, F_amount_, Limit_):

            try:
                Temp=Robot.get_market_state(F_Market)
                Current_Price[i]=float(Temp['data']['ticker']['last'])
                

                #print("Check sell order in btc")
                #print(Current_Price[i])
                F_result_Sell=Robot.query_order_pending(market=F_Market,offset=0, side=1, limit=10)
                sleep(0.5)
                F_result_Buy=Robot.query_order_pending(market=F_Market,offset=0, side=2, limit=10)
                #print(F_result_Buy)
                #print(F_result_Sell)
                
            except:
                continue

                
                
            

            try:
                if((F_result_Sell['data']['total']==0) and (F_result_Buy['data']['total']==0) and Current_Price[i] > Stop_Price ):
                    print("No Buy")
                    print("No Sell")
                    Robot.cancel_all_order(F_Market)
                    sleep(1)

                    Existed_Mojoodi=0
                    Res=Robot.query_position_pending(market=F_Market)
                    print(Res)
                    for item in Res['data']:
                        if(item['side']==2 and float(item['margin_amount'])>=(F_amount*Current_Price[i]/leverage[i]) and item['market']==F_Market):
                            Existed_Mojoodi=1
                            print('------------------------------------------------Existed Mojoofi --------')


                    F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount, Current_Price[i]-Limit*Current_Price[i])
                    sleep(0.5)
                    if(Existed_Mojoodi==1):
                        F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Current_Price[i]+Limit*Current_Price[i])
                    
                    
                    sleep(0.5)
                    F_result_Sell=Robot.query_order_pending(market=F_Market,offset=0, side=1, limit=10)
                    sleep(0.5)
                    F_result_Buy=Robot.query_order_pending(market=F_Market,offset=0, side=2, limit=10)
                    if(F_result_Sell['data']['total']!=0):
                        print('price')
                        print(F_result_Sell)
                        for item in F_result_Sell['data']['records']:
                            if item['market']==F_Market:
                                Sell_Price_Order[i]=float(item['price'])
                                print(Sell_Price_Order[i])
                    
                    sleep(0.5)
                    if(F_result_Buy['data']['total']!=0):
                        print('price')
                        print(F_result_Buy)
                        for item in F_result_Buy['data']['records']:
                            if item['market']==F_Market:
                                Buy_Price_Order[i]=float(item['price'])
                                print(Buy_Price_Order[i])
                    
                    print('Sell price order')
                    print(Sell_Price_Order[i])
                    print('Buy price order')
                    print(Buy_Price_Order[i])
                    
                    

                    
                    
                    

                elif((F_result_Sell['data']['total']==0) and (F_result_Buy['data']['total']!=0) and Current_Price[i] > Stop_Price and Current_Price[i]>0):
                    print("Buy")
                    print("No Sell")
                    
                    
                    #----------------------- Consider Mojoodi ---------------------
                    Existed_Mojoodi=0
                    Res=Robot.query_position_pending(market=F_Market)
                    for item in Res['data']:
                        if(item['side']==2 and float(item['margin_amount'])>=(F_amount*Current_Price[i]/leverage[i]) and item['market']==F_Market):
                            Existed_Mojoodi=1
                    sleep(0.5)    
                    
                    if(Existed_Mojoodi==1):
                        Robot.cancel_all_order(F_Market)
                        sleep(1)
                        if(Sell_Price_Order[i]>0 and Buy_Price_Order[i]<Sell_Price_Order[i]):
                            F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Sell_Price_Order[i]+Limit*Sell_Price_Order[i])
                            sleep(0.5)
                            F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount, Sell_Price_Order[i]-Limit*Sell_Price_Order[i])
                            sleep(0.25)
                        if(Sell_Price_Order[i]==0):
                            F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Current_Price[i]+Limit*Current_Price[i])
                            sleep(0.5)
                            F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount, Current_Price[i]-Limit*Current_Price[i])
                            sleep(0.25)
                    
                    
                        sleep(0.5)
                        F_result_Sell=Robot.query_order_pending(market=F_Market,offset=0, side=1, limit=10)
                        sleep(0.5)
                        F_result_Buy=Robot.query_order_pending(market=F_Market,offset=0, side=2, limit=10)
                        if(F_result_Sell['data']['total']!=0):
                            print('price')
                            print(F_result_Sell)
                            for item in F_result_Sell['data']['records']:
                                if item['market']==F_Market:
                                    Sell_Price_Order[i]=float(item['price'])
                                    print(Sell_Price_Order[i])
                    
                        sleep(0.5)
                        if(F_result_Buy['data']['total']!=0):
                            print('price')
                            print(F_result_Buy)
                            for item in F_result_Buy['data']['records']:
                                if item['market']==F_Market:
                                    Buy_Price_Order[i]=float(item['price'])
                                    print(Buy_Price_Order[i])
                        print('Sell price order')
                        print(Sell_Price_Order[i])
                        print('Buy price order')
                        print(Buy_Price_Order[i])
                    
                    
            
                

                elif((F_result_Sell['data']['total']!=0) and (F_result_Buy['data']['total']==0) and Current_Price[i] > Stop_Price and Current_Price[i]>0):
                    print("No Buy")
                    print("Sell")
                    sleep(0.5)
                    Existed_Mojoodi=0
                    Res=Robot.query_position_pending(market=F_Market)
                    for item in Res['data']:
                        if(item['side']==2 and float(item['margin_amount'])>=(F_amount*Current_Price[i]/leverage[i]) and item['market']==F_Market):
                            Existed_Mojoodi=1
                    
                    if(Existed_Mojoodi==1):
                        Robot.cancel_all_order(F_Market)
                        sleep(1)
                        if(Buy_Price_Order[i]>0 and Buy_Price_Order[i]<Sell_Price_Order[i]):
                            F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Buy_Price_Order[i]+Limit*Buy_Price_Order[i])
                            sleep(0.5)
                            F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount, Buy_Price_Order[i]-Limit*Buy_Price_Order[i])
                            sleep(0.25)
                        if(Buy_Price_Order[i]==0):
                            F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Current_Price[i]+Limit*Current_Price[i])
                            sleep(0.5)
                            F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_BUY, F_amount, Current_Price[i]-Limit*Current_Price[i])
                            sleep(0.25)

                        sleep(0.5)
                        F_result_Sell=Robot.query_order_pending(market=F_Market,offset=0, side=1, limit=10)
                        sleep(0.5)
                        F_result_Buy=Robot.query_order_pending(market=F_Market,offset=0, side=2, limit=10)
                        if(F_result_Sell['data']['total']!=0):
                            print('price')
                            print(F_result_Sell)
                            for item in F_result_Sell['data']['records']:
                                if item['market']==F_Market:
                                    Sell_Price_Order[i]=float(item['price'])
                                    print(Sell_Price_Order[i])
                    
                        sleep(0.5)
                        if(F_result_Buy['data']['total']!=0):
                            print('price')
                            print(F_result_Buy)
                            for item in F_result_Buy['data']['records']:
                                if item['market']==F_Market:
                                    Buy_Price_Order[i]=float(item['price'])
                                    print(Buy_Price_Order[i])
                        print('Sell price order')
                        print(Sell_Price_Order[i])
                        print('Buy price order')
                        print(Buy_Price_Order[i])
                    

                    
                    
                
                    
                    
            except:
                pass
            
            try:
                #-----------------------------------------Check Validity -------------------------------------------------
                if(Current_Price[i] < Stop_Price and Current_Price[i]>0 ):
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
                                if(str(item['market'])==F_Market_[0]):
                                    print('it is BTC')
                                    F_result=Robot.close_market(F_Market,item['position_id'])
                                    print(F_result)
                                    sleep(0.5)
                                if(str(item['market'])==F_Market_[1]):
                                    print('it is BTC')
                                    F_result=Robot.close_market(F_Market,item['position_id'])
                                    print(F_result)
                                
                        except:
                            print('can not cancell position buy Pending')
                                                
                    except:
                        print("Failed to cancel Mistake order")
            except:
                i=i+1
                continue
            
            try:
                Current_Price_Bit=0
                Temp=Robot.get_market_state('BTCUSDT')
                Current_Price_Bit=float(Temp['data']['ticker']['last'])
                if(Current_Price_Bit < Stop_Bit and Current_Price_Bit>0):
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
                        except:
                            print('can not cancell position buy Pending')
                                                
                    except:
                        print("Failed to cancel Mistake order")
            except:
                pass
            i=i+1
    except:
        pass
    sleep(3)
    #------------------------------------------- Save Sood --------------------------------
    

#F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_SELL, F_amount, Current_Price+1000)
#sleep(1)
#F_result=Robot.put_limit_order(F_Market, Robot.ORDER_DIRECTION_Buy, F_amount, Current_Price-1000)
#sleep(1)