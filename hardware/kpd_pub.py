import asyncio

import time
import threading
import paho.mqtt.client as mqtt
from gpiozero import Button
from gpiozero.output_devices import DigitalOutputDevice


row1 = DigitalOutputDevice(5, active_high=True)
row2 = DigitalOutputDevice(6, active_high=True)
row3 = DigitalOutputDevice(13, active_high=True)
row4 = DigitalOutputDevice(19, active_high=True)

block = False
rows = [row1,row2,row3]

broker = 'localhost'
client = mqtt.Client('pneumatics')



def on_log(client,userdata,level,buf):
   print('log: '+buf)

def on_connect(client, userdata, flags, rc):
   if rc == 0:
      print('[GUI] Connected OK')
      client.subscribe('spvm/actu_init')
   else:
      print('[GUI] Not connected : ', rc)

def on_message(client, userdata, msg):
   if msg.topic == 'spvm/actu_init':
      pass

client.on_connect = on_connect
client.on_message = on_message
client.on_log=on_log

print('[GUI] Connecting to broker : ', broker)
client.connect(broker)
client.loop_start()


class ButtN(Button):

   def __init__(self, btn_pin,name1,name2,name3):
      self.name = None
      self.name1 = name1
      self.name2 = name2
      self.name3 = name3

      self.btn_obj = Button(btn_pin,pull_up=False)
      self.btn_obj.hold_time = 1
      self.btn_obj.hold_repeat = 1
      self.btn_obj.when_held = self.button_held
      self.btn_obj.when_released = self.button_released
      self.btn_obj.when_pressed = self.button_pressed      
      self.c = 0

   def button_pressed(self):
      global block
      block = True
      if row1.is_active:
         self.name = self.name1
   
      elif row2.is_active:
         self.name = self.name2

      elif row3.is_active:
         self.name = self.name3

      print(self.name,' pressed')

      pressed_payload =  str(self.name)
      client.publish('pneumatics/pressed',pressed_payload)   
   
   def button_held(self):
      global block
      block = True
      self.c = self.c + 1

      held_payload =  str(self.name) + ',' + str(self.c)
      client.publish('pneumatics/held',held_payload)


   def button_released(self):
      global block
      print('Released', self.name,' after ',self.c,'seconds ')

      released_payload =  str(self.name) + ',' + str(self.c)

      client.publish('pneumatics/released',released_payload)

      self.c = 0
      self.name = None
      block = False


w = ButtN(12,'1','4','7')
x = ButtN(16,'2','5','8')
y = ButtN(20,'3','6','9')
z = ButtN(21,'A','B','C')


def toggle_pin():
   global block
   while True:  
      for ro in rows:
         ro.on()
         time.sleep(0.5)
         if block:
            break
         ro.off()
   time.sleep(1)
   
thr = threading.Thread(target= toggle_pin,daemon=True)
thr.start()

try:
   thr.join()

except KeyboardInterrupt:
   print('[INFO] Exitting ......')
   time.sleep(0.5)
   exit()