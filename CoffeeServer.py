#!/usr/bin/env python
import web
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import time

tree = ET.parse('user_data.xml')

urls = (
        '/status', 'status',
        '/waterstatus', 'water_status',
        '/heatstatus', 'heat_status',
        '/makecoffee', 'make_coffee',
        '/togglepower', 'toggle_power',
        '/users/(.*)', 'get_user'
        )

#setup gpios
GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
GPIO.setup(17,GPIO.OUT)#power
GPIO.setup(18,GPIO.OUT)#small size
GPIO.setup(27,GPIO.OUT)#medium size
GPIO.setup(22,GPIO.OUT)#large size
GPIO.setup(05,GPIO.IN)#Power led
GPIO.setup(06,GPIO.IN)#water level led
GPIO.setup(13,GPIO.IN)#heat level led


app = web.application(urls, globals())

class status:
    def GET(self):
        machine = Machine()
        status = machine.GetStatus()
        if status == True:
            return "Machine On"
        else:
            return "Machine Off"

class water_status:
    def GET(self):
        machine = Machine()
        status = machine.GetWaterStatus()
        if status == True:
            return "Water Full"
        else:
            return "Water Empty"

class heat_status:
    def GET(self):
        machine = Machine()
        status = machine.GetHeatStatus()
        if status == True:
            return "Hot"
        else:
            return "Cold"

class toggle_power:
    def GET(self):
        tools = Tools()
        tree = ET.parse('user_data.xml')
        tools.tree = tree
        input = web.input()
        if tools.CheckLogin(input.username, input.password):
            machine = Machine()
            machine.TurnOn()
            return "PowerToggle"
        else:
            return "Failed Login"

class make_coffee:
    def GET(self):
        tools = Tools()
        tree = ET.parse('user_data.xml')
        tools.tree = tree
        input = web.input()
        if tools.CheckLogin(input.username, input.password):
            print "Selecting Size " + input.size
            print "Making The Coffee"
            machine = Machine()
            machine.MakeCoffee(input.size)
            return "Making Your Coffee"
        else:
            return "Failed Login"

class get_user:
    def GET(self, user):
        for child in root:
            if child.attrib['id'] == user:
                return str(child.attrib)

class Tools:
    def CheckLogin(self, username, password):
        root = tree.getroot()
        for child in root:
            if child.attrib['username'] == username and child.attrib['password'] == password:
                print "Correct Password For User: " + username
                return True
            else:
                print "InCorrect Password For User: " + username
                return False

class Machine:
    def TurnOn(self):
        print "turning on"
        GPIO.output(17,GPIO.HIGH)
        time.sleep(5)
        GPIO.output(17,GPIO.LOW)

    def MakeCoffee(self, size):
        if size == "Large":
            GPIO.output(22,GPIO.HIGH)
            time.sleep(3)
            GPIO.output(22,GPIO.LOW)
        elif size == "Medium":
            GPIO.output(27,GPIO.HIGH)
            time.sleep(3)
            GPIO.output(27,GPIO.LOW)
        elif size == "Small":
            GPIO.output(18,GPIO.HIGH)
            time.sleep(3)
            GPIO.output(18,GPIO.LOW)

    def GetStatus(self):
        input = GPIO.input(05)
        if input:
            return True
        else:
            return False

    def GetWaterStatus(self):
        input = GPIO.input(06)
        if input:
            return True
        else:
            return False

    def GetHeatStatus(self):
        input = GPIO.input(13)
        if input:
            return True
        else:
            return False











if __name__ == "__main__":
    app.run()