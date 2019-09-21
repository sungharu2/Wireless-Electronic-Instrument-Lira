#!/usr/lib/python2.7
#-*- coding:utf-8 -*-

"""
2019 NHDK PROJECT MAIN CODE

터치스크린에서 멀티터치를 처리하기 위해 KIVY 라이브러리를 사용, KIVY 어플리케이션 동작
서버와 소켓통신을 하기 위한 socket 라이브러리 사용
아두이노에서 센서값을 받아오기 위해 시리얼 통신을 하도록 serial 라이브러리 사용

"""

print 'Start kivy Program'

import os

os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy

kivy.require('1.11.0')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.config import Config
from kivy.clock import Clock, mainthread
from random import random
from socket import *
import serial
import threading
import time

from kivy.core.window import Window

tickCount = 0
# Window.size = (200, 400)
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '400')
Config.write()

print 'Import complete'

# 서버와 소켓통신에 실패할 경우 netConnect 0으로 한 후 소켓통신 하지 않음
netConnect = 1
# usb 연결 시 생성되는 폴더로 시리얼 연결 후 usbConnect = 1, 실패 시 0
usbConnect = 0
try:
    ser = serial.Serial(
        '/dev/ttyACM0',
        9600,
    )
    print("Sensor Connected")
    usbConnect = 1
except:
    print("No Sensor Connected")
    usbConnect = 0


# 아두이노의 map 함수 구현, 처음 min~max 사이의 x값을 특정한 min~max 사이의 값으로 반환
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Position(FloatLayout):
    def on_touch_down(self, touch):
        global netConnect, usbConnect
        try:
            if netConnect == 1:
                sock = socket(AF_INET, SOCK_STREAM)
                #------------------------------------------------------
                sock.connect(('192.168.43.1', 5200))     # 서버 IP 지정
                #------------------------------------------------------
                msg = self.send_Serial(touch.x, touch.y)    # (x_y_시리얼값) 으로 전달
                sock.send(msg.encode('utf-8'))
                sock.recv(1024)
                sock.close()
                netConnect = 1
            else:
                pass

        except Exception, e:
            netConnect = 0
            print(e)

        # ud = User Data dictionary 각 터치들을 캔버스에 그리기 위해 그룹별로 관리, 색깔, 모양 지정
        ud = touch.ud
        # 그룹은 id값으로 분류
        ud['group'] = g = str(touch.uid)
        # x좌표에 따라 색깔 값 변경
        ud['color'] = map(touch.x, 0, 800, 0.0, 1.0)

        # 색깔 원 그리기
        with self.canvas:
            Color(ud['color'], 1, 1, mode='hsv', group=g)
            ud['lines'] = SmoothLine(circle=(touch.x, touch.y, 40), width=10, group=g)

        # 손을 뗄 때까지 grab 상태로 만듦
        touch.grab(self)

        print("touch down") # Log #####################
        return super(Position, self).on_touch_down(touch)

    def on_touch_move(self, touch):

        ud = touch.ud
        self.canvas.remove_group(ud['group'])   # 이전 그래픽 삭제 후 새 위치에 재생성
        # x좌표에 따라 색깔 값 변경
        ud['group'] = g = str(touch.uid)

        # 색깔 원 그리기
        ud['color'] = map(touch.x, 0, 800, 0.0, 1.0)
        with self.canvas:
            Color(ud['color'], 1, 1, mode='hsv', group=g)
            ud['lines'] = SmoothLine(circle=(touch.x, touch.y, 40), width=10, group=g)
    
        #print("touch move") # Log #####################
        return super(Position, self).on_touch_move(touch)

    def on_touch_up(self, touch):

        touch.ungrab(self)
        # 손을 떼기전 존재했던 터치 데이터 삭제
        ud = touch.ud
        self.canvas.remove_group(ud['group'])

        print("touch up")   # Log #####################
        return super(Position, self).on_touch_up(touch)

    @mainthread
    def update_label_connectionInfo(self):
        global net_text, netConnect

        threading.Timer(5, self.update_label_connectionInfo).start()    # 5초마다 인터넷 연결 여부 출력
        if netConnect == 1:
            net_text.text = ""
        else:
            net_text.text = "Offline"

    def return_Serial(self, x, y):
        global ser

        # 메시지 형식 : xxx_yyy_ser\n
        message = str(x) + '_' + str(y)
        if usbConnect == 1:
            if ser.readable:
                ser.write('a')  # 테스트 Send
                serValue = ser.readline()
                message += '_' + serValue
        else:
            message += '_100\n'

        print(message)
        return message

    def onclick_button(self):
        self.parent.parent.clear_widget()
        MyApp().build()

    def __init__(self):
        self.update_label_connectionInfo()


        super(Position, self).__init__()



class MyApp(App):
    def build(self):
        global net_text

        view = Position()
        layout= FloatLayout(size=(800, 600), cols=1, spacing=10, size_hint_y=None)
        view.add_widget(layout)

        net_text = Label(text="Connect to Touch", font_size='20sp')
        layout.add_widget(net_text)

        reconnect_button = Button(text="reconnect", font_size='15sp', size=[1, 1], center=[10, 10])
        reconnect_button.bind(on_release=Position.onclick_button)
        layout.add_widget(reconnect_button)

        return view


# if __name__ == '__main__':
MyApp().run()
