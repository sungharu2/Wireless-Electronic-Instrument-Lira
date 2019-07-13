#!/usr/lib/python2.7
print 'Start kivy Program'

import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy
kivy.require('1.11.0')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.config import Config
from random import random
from socket import *
import serial
import time

from kivy.core.window import Window
#Window.size = (200, 400)

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '400')
Config.write()


print 'Import complete'

usbConnect = 0
netConnect = 1
try:
    ser = serial.Serial(
        '/dev/ttyACM0',
        9600,
    )
    print("Sensor Connected")
    usbConnect = 1
except:
    print("No Sensor Connecting")
    usbConnect = 0

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Position(FloatLayout):
       
    def on_touch_down(self, touch):
	global netConnect, usbConnect
        try:
	    if netConnect == 1:	
                sock = socket(AF_INET, SOCK_STREAM)
                sock.connect(('192.168.137.157', 5200))
                msg = self.send_Serial(touch.x, touch.y)
	        #msg = "11_%d_%d\n" % (touch.x, touch.y)
                sock.send(msg.encode('utf-8'))
                s = sock.recv(1024)
                sock.close()
	        netConnect = 1
            else: 
	        pass

        except Exception, e:
	    netConnect = 0
            print(e)
	
            
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        ud['color'] = map(touch.x, 0, 800, 0.0, 1.0)
        
        with self.canvas:
            Color(ud['color'], 1, 1, mode='hsv', group=g)
            ud['lines'] = SmoothLine(circle=(touch.x, touch.y, 40), width=10, group=g)
            
        touch.grab(self)
        print("touch down")
        return True#super(Position, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):

        print("touch move")
        return super(Position, self).on_touch_move(touch)
    
    def on_touch_up(self, touch):       
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['group'])
        print("touch up")
        return super(Position, self).on_touch_up(touch)

    def update_touch_label(self, label, touch):
	global netConnect, usbConnect

        label.text = "x : %d, y : %d\n %s" % (touch.x, touch.y, "Connected" if netConnect == 1 else "Offline")
        #label.texture_update()

    def send_Serial(self, x, y):
	global ser

	message = str(x) + '_' + str(y)
	if usbConnect == 1:
	    if ser.readable:
                ser.write('a')
	        serStr = ser.readline()
	        serValue = serStr
	        serValue = serValue.replace('\n', '')
	        message += '_' + serValue
	else:
	    message += '_100' 
	message += '\n'
        print(message)
	return message
    
class MyApp(App):
    def build(self):
	
        return Position()


#if __name__ == '__main__':
MyApp().run()
