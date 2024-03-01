"""
Created on Thu Feb 10 22:38:47 2022

@author: naderrezazadeh
"""

#----------------------------  Coinex Bot  -----------------------------------
#-------------------------W


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


#-----------------------------------  ids  -----------------------------------
access_id = '7EAB85B8BE294B009A8119F53E1F4A0E'
secret_key = 'EDC73193092979E01FAF984F29B70CE3CDD22292A3879C88'


#------------------------------- Spot Variables--------------------------------
#---- Max Buy dollar
Max=30
#----- Buy per percent( amount=4 and percent=2 So All is 2*4=8)
amount=5
Market=["STARLUSDT","NFTBUSDT","ELONUSDT","MASKUSDT","ONEUSDT","TLMUSDT"]
Sood=0.025
Stop_Price=40490
#-----------------------------------------------------------------------------
#-----------------------------Features Params---------------------------------

#------------------- Max total buy in Features (in BTC)-----------------------
#----------- F_Max(Maximum Value of Btc Could Stay in َ)
F_Max=0.007
#----------- F_Max(Minimum Value that Could Stay in Account)
F_Min=0.002
#-----------minimu swing for operating
F_Margin=0.0049
#----------- Factor  buy*swing*F_Unit_Buy or Sell
F_Factor=1
F_Market="BTCUSDT"
F_Unit_Buy=0.001
F_Unit_Sell=0.001

#-------------------------  Controler Params ----------------------------------
Spot=1
Features=0
Kucoin_Trade_Listing=1
Address_File=r"C:\Users\Administrator\Desktop\CR\Report_Crypto.txt"
Address_File_Features=r"C:\Users\Administrator\Desktop\CR\Report_Crypto_F.txt"
Count_Of_Operation=10
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------






#-------------------------- Auto matic Parameter -----------------------------
#----------------------------- Spot Parameter --------------------------------
Factor=0
Head_Price=[]
Current_Price=[]
limits=[]
Volum=[]
Head_Price=np.zeros(len(Market))
Current_Price=np.zeros(len(Market))
limits=np.zeros(len(Market))
Volum=np.zeros(len(Market))

for i in range(0,len(Market)):
    limits[i]=Sood
    
    
coinex = Coinex(access_id, secret_key)


i=0
for market in Market:
    Head_Price[i]=float(coinex.get_last_price(market))
    Current_Price[i]=float(coinex.get_last_price(market))
    i=i+1

    
print(Head_Price)
print(Current_Price)
print(limits)
print(Volum)


#------------------------------------------------------------------------
sleep(5)
#------------------------------------ Features Parameter -----------------
F_Current_Price=0
F_Head_Price=0
F_Volum=0
robot = CoinexPerpetualApi(access_id, secret_key)
print(json.dumps(robot.ping(), indent=4))
F_result = robot.get_market_state(market=F_Market)
print(F_result['data']['ticker']['last'])
F_Price=F_result['data']['ticker']['last']
if(F_Head_Price==0):
    F_Head_Price=float(F_Price)
print("Current order")
F_result=robot.query_position_pending()
print(F_result['data'][0]['position_id'])
print(json.dumps(F_result, indent=4))

#------------------------------ End of Global Variables ----------------------
#-----------------------------------------------------------------------------
#-------------------------------- Listing Kucoin ----------------------------
response = requests.get("https://www.kucoin.com/_api/cms/articles?page=1&pageSize=10&category=listing&lang=en_US")
jsoncode = response.json()
options = jsoncode['items']
Old_Kucoin=options[len(options)-1]['title']
Current_Kucoin=Old_Kucoin
Listing_Buy=40
#------------------------------------ Feature  Function------------------------
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------
def Features_Trading():
    print("------------------------- Features ----------------------")
    global robot,Stop_Price,F_Head_Price,F_Current_Price,F_Volum,Address_File_Features,F_Max,F_Min,Features
    result=" "
    Mojoodi=0
    try:
        #F_result = robot.get_market_state(market=F_Market)
        #print(result['data']['ticker']['last'])
        F_result = robot.query_position_pending(market=F_Market)
        F_Current_Price=float(F_result['data'][0]['latest_price'])
        #Mojoodi=Mojoodi*float(F_result['data'][0]['latest_price'])/(float(F_result['data'][0]['leverage']))+(float(F_result['data'][0]['profit_unreal']))
        Mojoodi=float(F_result['data'][0]['close_left'])
        F_Volum=Mojoodi*float(F_result['data'][0]['latest_price'])/(float(F_result['data'][0]['leverage']))+(float(F_result['data'][0]['profit_unreal']))
    except:
        sleep(1)
        try:
            robot = CoinexPerpetualApi(access_id, secret_key)
            print(json.dumps(robot.ping(), indent=4))
            F_result = robot.query_position_pending(market=F_Market)
            F_Current_Price=float(F_result['data'][0]['latest_price'])
            #Mojoodi=Mojoodi*float(F_result['data'][0]['latest_price'])/(float(F_result['data'][0]['leverage']))+(float(F_result['data'][0]['profit_unreal']))
            Mojoodi=float(F_result['data'][0]['close_left'])
            F_Volum=Mojoodi*float(F_result['data'][0]['latest_price'])/(float(F_result['data'][0]['leverage']))+(float(F_result['data'][0]['profit_unreal']))
            F_Head_Price=F_Current_Price
            
                
        except:
            Mojoodi=0
            F_Current_Price=0
            F_Head_Price=0
            
    
    if(F_Current_Price!=0):
        print("Current_Price is: ")
        print(F_Current_Price)
        print("Head Price is: ")
        print(F_Head_Price)
        print("Existed in Btc(Mojoodi): ")
        print(Mojoodi)
        print("Existed Volum: ")
        print(F_Volum)
        print("Maximum in Btc(Mojoodi): ")
        print(F_Max)
            
           
            
            
        #------------------------------------  Buy Section ------------------------
        if(F_Current_Price + F_Margin*F_Head_Price < (F_Head_Price )  and F_Current_Price>0 and Mojoodi < F_Max):
                
            print("open Buy  Features Section:")
            print("Current_Price is: ")
            print(F_Current_Price)
            print("Head Price is: ")
            print(F_Head_Price)
                
            F_Count_of_Buy=abs((100*((F_Head_Price-F_Current_Price)/(F_Head_Price))*F_Factor))
            print("Count of Buy")
            print(F_Count_of_Buy)
            if(F_Count_of_Buy >0 ):
                print("Count of Buy unit")
                print(F_Count_of_Buy)
                F_amount=F_Count_of_Buy*(F_Unit_Buy)
                print("Amount of Buy")
                print(F_amount)
                F_amount=str(F_amount)
                
                F_result=robot.put_market_order(F_Market, robot.ORDER_DIRECTION_BUY, F_amount)
               
                print(F_result)
                F_Head_Price=F_Current_Price
                try:
                    with open(Address_File_Features, "a") as f:
                        f.write("Success Feature Buy Token: "+str(F_Market)+", Dolar: "+str(F_Count_of_Buy*8)+", in Price: "+str(F_Current_Price)+", Total:"+str( F_Volum))
                        f.write("\n")
                        f.close()
                except:
                    pass
               
                    #with open(Address_File_Features, "a") as f:
                     #   f.write("Error Feature Buy Token: "+str(F_Market)+"Dolar: "+str(F_Count_of_Buy*8)+" in Price: "+str(F_Current_Price)+"Total:"+str( F_Volum))
                      #  f.write("\n")
                       # f.write(str(result))
                        #f.write("\n")
                        #f.close()
                     
                
                
               
                
            #---------------------------------- Sell Section ----------------------------    
        if(F_Current_Price > F_Head_Price+ F_Margin*F_Head_Price and F_Current_Price>0 ):
            
            #---------------   Type 1 is Sell    and  Type 2  ia Buy)
            if(int(F_result['data'][0]['type'])==2):
                
                F_Count_of_Sell=abs((100*((F_Current_Price-F_Head_Price)/(F_Current_Price))*F_Factor))
                print("Open Sell Features Section")
                print("Count of Sell unit")
                print(F_Count_of_Sell)
                F_amount=F_Count_of_Sell*(F_Unit_Sell)
                print("Mojoodi")
                print(Mojoodi)
                print("Mojoodi-F_amount")
                print(Mojoodi-F_amount)
                if(Mojoodi-F_amount > F_Min):
                
                            
                    try:
                        F_amount=str(F_amount)
                        print("Amount of Sell")
                        print(F_amount)
                        robot.put_market_order(F_Market, robot.ORDER_DIRECTION_SELL, F_amount)
                        F_Volum=F_Volum-F_amount*F_Current_Price
                        F_Head_Price=F_Current_Price
                        print("Write to file")
                        try:
                            with open(Address_File_Features, "a") as f:
                                f.write("Success Feature Sell Token: "+str(F_Market)+", Dolar: "+str(F_Count_of_Sell*8)+", in Price: "+str(F_Current_Price)+", Total:"+str( F_Volum))
                                f.write("\n")
                                f.close()
                        except:
                            pass
                        
                    except:
                        try:
                            with open(Address_File_Features, "a") as f:
                                f.write("Error Feature Sell Token: "+str(F_Market)+", Dolar: "+str(F_Count_of_Sell*8)+", in Price: "+str(F_Current_Price)+", Total:"+str( F_Volum))
                                f.write("\n")
                                f.write(str(result))
                                f.write("\n")                    
                                f.close()
                        except:
                            pass
            
        if(F_Current_Price < Stop_Price and F_Current_Price>0):
            F_result=robot.query_position_pending()
            position_id=F_result['data'][0]['position_id']
            robot.close_market(F_Market, position_id)
            Features=0
        if(F_Current_Price < Stop_Price-70 and F_Current_Price>0 ):
            
            robot.put_market_order(F_Market, robot.ORDER_DIRECTION_SELL, 40)
            Features=0
        


#----------------------------------Spot Function -----------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def Spot_Trading():
    print("------------------------- Spot ----------------------")
    global coinex,Market,Volum,Max,Address_File,Spot
    i=0
    result="";
    for market in Market:
        try:
            Current_Price[i]=float(coinex.get_last_price(market))
        except:
            Current_Price[i]=0
            coinex = Coinex(access_id, secret_key)
            i=i+1
            continue
        
        
        if(Current_Price[i]!=0):
            #------------------------    market price    -----------------------------
            print(market)
            print(Head_Price[i])
            print(Current_Price[i])
            print(limits[i]*Head_Price[i])
            print(Volum[i])
            print(Max)
                
                
                
            #-------------------  Buy Section --------------------
            if(Current_Price[i] + limits[i]*Head_Price[i] < Head_Price[i] and Current_Price[i]>0 and Volum[i] <Max):
                print("open buy Section")
                Factor=100*abs( (Head_Price[i]-Current_Price[i])/(Head_Price[i]))
                value=Factor*amount
                print("Factor: ")
                print(Factor)
                print("Value Buy: ")
                print(value)
                
                try:
                    result=coinex.market_buy(market, value)
                    print(result)
                    Message=result['message']
                    if(result['message']=='Less than minimum requirement' or result['message']=='Balance Insufficient'):
                        print("Error low Money than minimum or Balance Insufficient")
                    if(result['message']=='Balance Insufficient'):
                        Volum[i]=Max
                        
                        
                  
                    if(result['message']=='Success'):
                        print("Success")
                        Volum[i]=Volum[i]+value
                        Head_Price[i]=Current_Price[i]
                        try:
                            with open(Address_File, "a") as f:
                                f.write("Success Buy Token: "+str(market)+", Dolar: "+str(value)+" in Price: "+str(Current_Price[i])+", Total:"+str(Volum[i])+" , Message: "+Message)
                                f.write("\n")
                                f.close()
                        except:
                            pass
                
                   
                    
                    
                    #print(Head_Price[i] +limits[i]*Head_Price[i])
                    #print(Current_Price[i])
                    
    
                except:
                    print("Error  Buy")
                    try:
                        with open(Address_File, "a") as f:
                            f.write("Error Buy Token: "+str(market)+", Dolar: "+str(value)+" in Price: "+str(Current_Price[i])+", Total:"+str(Volum[i]))
                            f.write("\n")
                            f.write(str(result))
                            f.write("\n")
                            f.close()
                    except:
                        pass
                    
                
                #-------------------  Sell Section --------------------
            if(Current_Price[i] > Head_Price[i] +limits[i]*Head_Price[i] and Current_Price[i]>0):
                print("open Sell Section")
                Factor=100*abs( (Current_Price[i]-Head_Price[i])/(Head_Price[i]))
                value=Factor*amount
                print("Factor: ")
                print(Factor)
                print("Value Sell: ")
                print(value)
               
                
                try:
                    result=coinex.market_sell(market, value)
                    print(result)
                    Message=result['message']
                    if(result['message']=='Less than minimum requirement' or result['message']=='Balance Insufficient'):
                        print("Error low Money than minimum or Balance Insufficient")
                        if(result['message']=='Balance Insufficient'):
                            #Head_Price[i]=Current_Price[i]
                            try:
                                with open(Address_File, "a") as f:
                                    f.write("Error Sell Token"+str(market)+", Dolar: "+str(value)+" in Price: "+str(Current_Price[i])+ ", Message: "+str(Message))
                                    f.write("\n")
                                    f.close
                            except:
                                pass
                            
                       
                       
                  
                    if(result['message']=='Success'):
                        print("Success")
                        Volum[i]=Volum[i]-value
                        Head_Price[i]=Current_Price[i]
                        try:
                            with open(Address_File, "a") as f:
                                f.write("Success Sell Token: "+str(market)+", Dolar: "+str(value)+" in Price: "+str(Current_Price[i])+", Total:"+str(Volum[i])+" , Message: "+str(Message))
                                f.write("\n")
                                f.close()
                        except:
                            pass
                
                    
                    
                    
                except:
                    print("Error  Selll")
                    try:
                        with open(Address_File, "a") as f:
                            f.write("Error Sell Token: "+str(market)+", Dolar: "+str(value)+" in Price: "+str(Current_Price[i])+", Total:"+str(Volum[i]))
                            f.write("\n")
                            f.write(str(result))
                            f.write("\n")
                            f.close()
                    except:
                        pass
                  
            
                      
            i=i+1
            sleep(2)
        try:
            BTC_Last=float(coinex.get_last_price('BTCUSDT'))
            if(BTC_Last < Stop_Price ):
                Spot=0
        except:
            pass
        
 
    
 
def Kucoin_Listing():
    global Old_Kucoin,Current_Kucoin,Listing_Buy,Address_File
    try:
        response = requests.get("https://www.kucoin.com/_api/cms/articles?page=1&pageSize=10&category=listing&lang=en_US")
        jsoncode = response.json()
        options = jsoncode['items']
        Current_Kucoin=options[len(options)-1]['title']
    except:
        Current_Kucoin=Old_Kucoin
        pass
    if(Current_Kucoin!=Old_Kucoin):
        Temp_=Current_Kucoin.split('(');
        Temp=Temp_[1]
        Temp__=Temp.split(')');
        token=Temp__[0]
        result=coinex.market_buy(token,Listing_Buy)
        Old_Kucoin=Current_Kucoin
        try:
            with open(Address_File, "a") as f:
                f.write("\n")
                f.write("  "+str(token)+"  "+str(Listing_Buy)+"  "+str(result))
                f.write("\n")           
                f.close()
            pass
        except:
            pass
        

if __name__ == "__main__":
    
    
    
    
    
 
    sleep(10)
    while (True):
        
        if(Spot==1):
            Spot_Trading()
        
        sleep(5)
       
        
        if(Features==1):
            Features_Trading()
        
        sleep(3)
        if(Kucoin_Trade_Listing==1):
            Kucoin_Listing()
            
        
    
    
    
    
        #print(Head_Price[i])
        
        
        
        
      