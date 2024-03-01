from msilib.schema import Error
from typing import Counter
from xmlrpc.client import Marshaller
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


access_id_F='A35CD912B440463680985119FD5EC813'
secret_key_F='A150F6BE31FA70396A48F262647B24AFB693855A3D63463A'


Robot_F = CoinexPerpetualApi(access_id_F, secret_key_F)



Market="BTTUSDT"
#----------------------------------------------------------------

Limit=0.005
# Countof Token price*leverage  (20 mana)
F_amount=10000000
leverage=10
# Countof Token price*leverage  (20 mana)
Begin_Buy_F=0
#in $

Stop_Price_Up=0.0000029
Stop_Price_Down=0.0000008

#------------------------------
#------------------------------
Current_Price=0
Touch_Price_Up=0
Touch_Price_Down=0
Sell_Price_Order=0
Buy_Price_Order=0
Sell_Order_id=0
minimum_Mojoodi_Spot=60

if(Begin_Buy_F!=0):
    Robot_F.put_market_order(market=Market, side=1, amount=Begin_Buy_F)
    sleep(1)



#result_sell=Robot_S.limit_sell(Market, Begin_Buy_S, Stop_Price_Up)
#if(result_sell['code']==0):
#    Sell_Order_id=int(result_sell['data']['id'])
#    print(Sell_Order_id)




def Target():
    global Robot_F,leverage
    global Limit,F_amount,leverage,Market
    global Stop_Price_Up,Stop_Price_Down,Touch_Price_Up,Touch_Price_Up,Current_Price
    global Buy_Price_Order,Sell_Price_Order
    try:
        Current_Price=0
        Temp=Robot_F.get_market_state(Market)
        Current_Price=float(Temp['data']['ticker']['last'])
        print(Current_Price)
        if(Current_Price >= Stop_Price_Up and Current_Price>0):
            Touch_Price_Up=1; Touch_Price_Down=0
            pass
          
        if(Current_Price <= Stop_Price_Down and Current_Price>0):
            Touch_Price_Up=0; Touch_Price_Down=1
            pass
            

        #print("Check sell order in btc")
        #print(Current_Price[i])
        F_result_Sell=Robot_F.query_order_pending(market=Market,offset=0, side=1, limit=10)
        sleep(0.5)
        F_result_Buy=Robot_F.query_order_pending(market=Market,offset=0, side=2, limit=10)
    except:
        pass

    try:
        if((F_result_Sell['data']['total']==0) and (F_result_Buy['data']['total']==0) and Current_Price < Stop_Price_Up and Current_Price>Stop_Price_Down ):
            print("No Buy")
            print("No Sell")
            Robot_F.cancel_all_order(Market)
            sleep(1)

            Existed_Mojoodi=0
            Res=Robot_F.query_position_pending(market=Market)
            print(Res)
            for item in Res['data']:
                if(item['side']==1 and float(item['margin_amount'])>=(F_amount*Current_Price/leverage) and item['market']==Market):
                    Existed_Mojoodi=1
                    print('------------------------------------------------Existed Mojoofi --------')
            F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_SELL, F_amount, Current_Price+Limit*Current_Price)
            
            sleep(0.5)
            if(Existed_Mojoodi==1):
                F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_BUY, F_amount, Current_Price-Limit*Current_Price)
                
                sleep(0.5)
                F_result_Sell=Robot_F.query_order_pending(market=Market,offset=0, side=1, limit=10)
                sleep(0.5)
                F_result_Buy=Robot_F.query_order_pending(market=Market,offset=0, side=2, limit=10)
                if(F_result_Sell['data']['total']!=0):
                    print('price')
                    print(F_result_Sell)
                    for item in F_result_Sell['data']['records']:
                        if item['market']==Market:
                            Sell_Price_Order=float(item['price'])
                            print(Sell_Price_Order)
                
                sleep(0.5)
                if(F_result_Buy['data']['total']!=0):
                    print('price')
                    print(F_result_Buy)
                    for item in F_result_Buy['data']['records']:
                        if item['market']==Market:
                            Buy_Price_Order=float(item['price'])
                            print(Buy_Price_Order)
                
                print('Sell price order')
                print(Sell_Price_Order)
                print('Buy price order')
                print(Buy_Price_Order)
                pass
            if(Existed_Mojoodi==0):
                pass
   

        elif((F_result_Sell['data']['total']==0) and (F_result_Buy['data']['total']!=0) and Current_Price < Stop_Price_Up and Current_Price>Stop_Price_Down ):
            print("Buy")
            print("No Sell")
                    
                    
            #----------------------- Consider Mojoodi ---------------------
            Existed_Mojoodi=0
            print('hhh')
            Res=Robot_F.query_position_pending(market=Market)
            print('hhh')
            print(Res)
            for item in Res['data']:
                if(item['side']==1 and float(item['margin_amount'])>=(F_amount*Current_Price/leverage) and item['market']==Market):
                    Existed_Mojoodi=1
                    print('existed')
                    sleep(0.5)    
                    
                    if(Existed_Mojoodi==1):
                        Robot_F.cancel_all_order(Market)
                        sleep(1)
                        if(Sell_Price_Order>0 and Buy_Price_Order<Sell_Price_Order):
                            F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_SELL, F_amount, Sell_Price_Order+Limit*Sell_Price_Order)
                            sleep(0.5)
                            F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_BUY, F_amount, Sell_Price_Order-Limit*Sell_Price_Order)
                            sleep(0.25)
                        if(Sell_Price_Order==0):
                            F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_SELL, F_amount, Current_Price+Limit*Current_Price)
                            sleep(0.5)
                            F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_BUY, F_amount, Current_Price-Limit*Current_Price)
                            sleep(0.25)
                    
                    
                        sleep(0.5)
                        F_result_Sell=Robot_F.query_order_pending(market=Market,offset=0, side=1, limit=10)
                        sleep(0.5)
                        F_result_Buy=Robot_F.query_order_pending(market=Market,offset=0, side=2, limit=10)
                        if(F_result_Sell['data']['total']!=0):
                            print('price')
                            print(F_result_Sell)
                            for item in F_result_Sell['data']['records']:
                                if item['market']==Market:
                                    Sell_Price_Order=float(item['price'])
                                    print(Sell_Price_Order)
                    
                        sleep(0.5)
                        if(F_result_Buy['data']['total']!=0):
                            print('price')
                            print(F_result_Buy)
                            for item in F_result_Buy['data']['records']:
                                if item['market']==Market:
                                    Buy_Price_Order=float(item['price'])
                                    print(Buy_Price_Order)
                        print('Sell price order')
                        print(Sell_Price_Order)
                        print('Buy price order')
                        print(Buy_Price_Order)
                        pass
                    if(Existed_Mojoodi==0):
                        print('return 0')
                        pass


        elif((F_result_Sell['data']['total']!=0) and (F_result_Buy['data']['total']==0) and Current_Price < Stop_Price_Up and Current_Price>Stop_Price_Down ):
            print("No Buy")
            print("Sell")
            sleep(0.5)
            Existed_Mojoodi=0
            Res=Robot_F.query_position_pending(market=Market)
            print(Res)
            for item in Res['data']:
                if(item['side']==1 and float(item['margin_amount'])>=(F_amount*Current_Price/leverage) and item['market']==Market):
                    Existed_Mojoodi=1
            
            if(Existed_Mojoodi==1):
                Robot_F.cancel_all_order(Market)
                sleep(1)
                if(Buy_Price_Order>0 and Buy_Price_Order<Sell_Price_Order):
                    F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_SELL, F_amount, Buy_Price_Order+Limit*Buy_Price_Order)
                    sleep(0.5)
                    F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_BUY, F_amount, Buy_Price_Order-Limit*Buy_Price_Order)
                    sleep(0.25)
                if(Buy_Price_Order==0):
                    F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_SELL, F_amount, Current_Price+Limit*Current_Price)
                    sleep(0.5)
                    F_result=Robot_F.put_limit_order(Market, Robot_F.ORDER_DIRECTION_BUY, F_amount, Current_Price-Limit*Current_Price)
                    sleep(0.25)

                sleep(0.5)
                F_result_Sell=Robot_F.query_order_pending(market=Market,offset=0, side=1, limit=10)
                sleep(0.5)
                F_result_Buy=Robot_F.query_order_pending(market=Market,offset=0, side=2, limit=10)
                if(F_result_Sell['data']['total']!=0):
                    print('price')
                    print(F_result_Sell)
                    for item in F_result_Sell['data']['records']:
                        if item['market']==Market:
                            Sell_Price_Order=float(item['price'])
                            print(Sell_Price_Order)
            
                sleep(0.5)
                if(F_result_Buy['data']['total']!=0):
                    print('price')
                    print(F_result_Buy)
                    for item in F_result_Buy['data']['records']:
                        if item['market']==Market:
                            Buy_Price_Order=float(item['price'])
                            print(Buy_Price_Order)
                print('Sell price order')
                print(Sell_Price_Order)
                print('Buy price order')
                print(Buy_Price_Order)
                pass
            if(Existed_Mojoodi==0):
                pass


    except:
        pass
    pass                


Counter=0
while(True):
    Target()
    
     
    
    sleep(3)
    
    
