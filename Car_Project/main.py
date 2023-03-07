import time
import network
import ubinascii
import machine 
from machine import PWM, Pin
from umqtt.simple import MQTTClient
from machine import I2C
from imu import MPU6050
import utime
from mfrc522 import MFRC522

servoPin1 = PWM(Pin(16))
servoPin1.freq(50)
trig = machine.Pin(32,machine.Pin.OUT)
echo = machine.Pin(35,machine.Pin.IN)

motor1a = machine.Pin(26, machine.Pin.OUT)
motor1b = machine.Pin(27, machine.Pin.OUT)
motor2a = machine.Pin(12, machine.Pin.OUT)
motor2b = machine.Pin(14, machine.Pin.OUT)

led = machine.Pin(22, machine.Pin.OUT)    #設定開發板上的 LED(Pin22) 
MPU = machine.Pin(2, machine.Pin.OUT)
led.value(1)

i2c = I2C(0, sda=Pin(13), scl=Pin(15), freq=20000)
led = Pin(22, Pin.OUT)
imu = MPU6050(i2c)
memo=0
#functions
def distance():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    while echo.value() == 0:
        pass
    while echo.value() == 1:
        ts = time.ticks_us()
        while echo.value() == 1:
            pass
        te = time.ticks_us()
        tc = te - ts
        distance = round((tc*170)/10000, 2)
    return distance

def forward():   #向前
    led.value(1)
    motor1a.value(0)
    motor1b.value(1)
    motor2a.value(0)
    motor2b.value(1)
    
def backward():   #向後
    led.value(1)
    motor1a.value(1)
    motor1b.value(0)
    motor2a.value(1)
    motor2b.value(0)
    
def right():      #左轉
    led.value(1)
    motor1a.value(0)
    motor1b.value(1)
    motor2a.value(1)
    motor2b.value(0)

def left():     #右轉
    led.value(1)
    motor1a.value(1)
    motor1b.value(0)
    motor2a.value(0)
    motor2b.value(1) 
    
def stop():     #停止
    led.value(0)
    motor1a.value(0)
    motor1b.value(0)
    motor2a.value(0)
    motor2b.value(0)

mqtt_server="mqttgo.io"
client_id = ubinascii.hexlify(machine.unique_id())
topic=b'move'
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False )
sta_if.active(True)
sta_if.disconnect()
sta_if.connect('UBUB', '00001111')
msg =0
#speaker = PWM(Pin(23))
#speaker.duty_u16(0)
while not sta_if.isconnected():
    pass

print("connected")
led.value(0)
utime.sleep(0.5) #LED LIGHT 0.5 when connect
led.value(1)

client = MQTTClient(
    client_id="client0706bd", 
    keepalive=5,
    server=mqtt_server,#"test.mosquitto.org", 
    ssl=False)
client.connect()

def servo(degrees):  #SG90函數
    if degrees > 180:degrees=180
    if degrees < 0:degrees=0
    maxDuty=9000    # 我們將傳遞 1000-9000 微秒之間的值，這對應於PWM.duty_u16()方法中手臂的 0-180 度位置移動。
    minDuty=1000    #
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    servoPin1.duty_u16(int(newDuty))
    
def get_msg(topic, data):
    global msg
    print(data)
#    msg = int(data,10)
    msg=data    
    
def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub, topic_sub2, topic_sub3
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(get_msg)
  client.connect()
  client.subscribe(topic)
  print('Connected to %s , subscribed to %s' % (mqtt_server, topic))
  return client

client.set_callback(get_msg)
client.subscribe(b'move')
try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
counter = 0
stop()
def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
              
reader = MFRC522(sck=18,miso=19,mosi=23,cs=5,rst=17)
stol=1
MPU.value(1)
while True:
    (stat, tag_type) = reader.request(reader.REQIDL)   # 搜尋 RFID 卡片
    
    if MPU.value()==1 and memo==0:    
        x1 = abs(round(imu.accel.x,2)*100)
        y1 = abs(round(imu.accel.y,2)*100)
        z1 = abs(round(imu.accel.z,2)*100)
        print(x1,y1,z1)
        memo=1
    
    if MPU.value()==1:
        x = abs(round(imu.accel.x,2)*100)
        y = abs(round(imu.accel.y,2)*100)
        z = abs(round(imu.accel.z,2)*100)
        print(x,y,z)
        if ((abs(x-x1) or abs(y-y1) or abs(z-z1)) > 10)  :
            print(memo,"FUCK YOU")
            if stol ==1 :
                MPU.value(0)
                utime.sleep(0.5)
                MPU.value(1)
    if stat == reader.OK:      # 找到卡片
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card_num = uidToString(uid)
                print(".....卡片號碼： %s" % card_num)
                if  card_num == '20722E90':   #'7A811D60':
                    print("卡片正確，取消防盜") 
                    led.value(1)   # 讀到授權的卡號後點亮綠色 LED
                    utime.sleep(1)       # 亮 2 秒鐘
                    led.value(0)   # 綠燈滅
                    stol=0
                    for degree in range(0,90,1):	#0-180度
                        servo(degree)
                        time.sleep(0.01)
                    utime.sleep(1)    
                    for degree in range(90,0,-1):	#0-180度
                        servo(degree)
                        time.sleep(0.01)
                                                                    
                else:
                    print(".....卡片錯誤.....")
                    led.value(1)    # 讀到非授權的卡號後點亮紅色 LED
                    utime.sleep(1)      # 亮 2 秒鐘
                    led.value(0)    #紅燈滅
            else:
                print(".....授權錯誤.....")
            
    dist = distance()
    print('distance:', dist, 'cm')
    if dist<20:
        print("stop")
        msg=b'S'
        stop()
        msg=b''
    utime.sleep(0.2)
    
    # print all values
    
    client.check_msg()
#    print(msg)
#    client.ping()
    time.sleep(0.2)
    stop()
    if msg ==b'F':
        forward()      #向前  
        utime.sleep(2)
        stop()
        
        msg=b''
    elif msg ==b'B':                                          
        backward()        
        utime.sleep(2)
        stop()
        
        msg=b''
    elif msg ==b'L':
        left()        
        utime.sleep(0.2)
        stop()
        
        msg=b''
    elif msg ==b'R':
        right()        
        utime.sleep(0.2)
        stop()
        
        msg=b''
    elif msg ==b'LF':
        forward()      #向前  
        
    elif msg ==b'LB':                                          
        backward()        
        
    elif msg ==b'LL':
        left()        
        
    elif msg ==b'LR':
        right()
    elif msg ==b'stol':
        stol=1
        print("防盜啟動")
        msg =b''
    elif msg ==b'exit':
        break
        
    else:
        stop()
        msg=b''
