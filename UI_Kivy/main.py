import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty
import threading
import time
import math

import sys
import requests
import json

from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior

class CustButton(ButtonBehavior, AsyncImage):
    pass
class client():
    def __init__(self,credit):
        self.__credit__=credit
    def getCredit(self):
        return self.__credit__
    def setCredit(self,credit):
        self.__credit__=credit


class machine():

    def __init__(self, OzPrice, Oz, total):
        self.__OzPrice__ = OzPrice
        self.__Oz__ = Oz
        self.__total__ = total



    def getBalance(self):
        return self.__total__
    def getOzPrice(self):
        return (self.__OzPrice__)
    def getOz(self):
        return (self.__Oz__)

    def setOz(self,x):
         self.__Oz__=x
    def setOzPrice(self,x):
         self.__OzPrice__=x

    def setBalance(self, y):
        self.__total__=  y


    def updateBalance(self, y, x):
        self.__total__=  (y*x)


    balance = property(getBalance, setBalance)
class FloatLayout(FloatLayout):

    acc = machine(0.4, 0.0, 0.0)
    user=client(0)

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)

    def upd_ltxt(self):
        response = requests.get("http://localhost:1337/machines/1")
        if (response.status_code == 200):
            x= response.json()["Liter_price"]
            y=response.json()["brand_beer_image"][0]["url"]
            self.ids.btn_id.source= "http://localhost:1337"+y
            self.ids.btn_2.source= "http://localhost:1337"+y
            self.ids.OzPrice_label.text= str(x)+"DT/L"
            self.acc.setOzPrice(x/33.814)
            print(self.acc.getOzPrice())
        elif (response.status_code == 404):
            print("Result not found!")
    def deterministic(self):
        threading.Thread(target=self.OzEmulator).start()
    def OzEmulator(self):
        self.ids.btn_id.disabled=True
        print(self.acc.getOzPrice())
        for i in range(3):
            if (self.user.getCredit()-self.acc.getBalance()>(self.acc.getOzPrice()*(self.acc.getOz()+10))):
                self.acc.setOz(self.acc.getOz()+10)
                self.ids.Oz_label.text=str(round((self.acc.getOz()*0.0295735),2))  +"Liter"
                self.acc.updateBalance(self.acc.getOzPrice(), self.acc.getOz())
                self.ids.balance_label.text=str(round(self.acc.getBalance(),2))+ "DT"
                print(str(self.acc.getBalance())+" Total")
                print(str(self.acc.getOz())+ "OZ")
                print(str(self.acc.getOzPrice())+" Price")
                print("_________________________________________")
                time.sleep(0.5)
        self.updateAccount()
        self.resetMachine()

        self.ids.btn_id.disabled=False

    def newClient(self):
        response = requests.get("http://localhost:1337/clients/1")
        if (response.status_code == 200):
            j= response.json()['Balance']
            c=client(float(j))
            self.user=c
            print(j)



    def updateAccount(self):
        new_balance=self.user.getCredit()-self.acc.getBalance()
        task = {"Balance":str(new_balance)}
        resp = requests.put('http://localhost:1337/clients/1', json=task)
        if resp.status_code != 200:
            print('Error')
        print("transaction made")
    def resetMachine(self):
        self.acc.setOz(0.0)
        self.ids.Oz_label.text="0.0"+" L"
        self.acc.setBalance(0.0)
        self.ids.balance_label.text="0.0"+" DT"
        print("reset")




"""
    def update_balance(self, *args):
        self.ids.balance_label.text= str(round(self.acc.getBalance(),2))+ "DT"
        = str(round(self.acc.getOz(),2))+ "OZ" """

"""    def realTimeEmulator(self):
        p1 = Process(target=self.acc.OzEmulator())
        p1.start()
        Clock.schedule_interval(self.update_balance, 0.1)

    def iterator(self):
        for i in range(6):
            self.realTimeEmulator()
"""

class floatlayout(App):

    def build(self):
        f=FloatLayout()
        f.upd_ltxt()
        return f

fl= floatlayout()
fl.run()
