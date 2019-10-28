import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import sys
import json
import uuid

broker = 'c6jrp91.mqtt.iot.gz.baidubce.com'
port = 1883
username = 'c6jrp91/myRaspberry'
password = '5jv27fkyv36ukhta'
clientid = 'myRaspberry_' + str(uuid.uuid4())
topic = '$baidu/iot/shadow/myRaspberry/update/accepted'

def on_connect(client, userdata, rc):
    print('Connected. Client id is: ' + clientid)
    client.subscribe(topic)
    print('Subscribed to topic: ' + topic)

def on_message(client, userdata, msg):
    msg = str(msg.payload, 'utf-8')
    result = json.loads(msg)
    direction = result["reported"]["direction"]
    if direction == "stop":
        reset()
    elif direction == "left":
        left()
    elif direction == "right":
        right()
    elif direction == "front":
        front()
    elif direction == "back":
        back()
    print('MQTT message received: ' + msg)
    if msg == 'exit':
        sys.exit()

ENA = 0;
ENB = 0;

def init():
    global ENA, ENB
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setup(38, GPIO.OUT)
    ENA = GPIO.PWM(36, 100)
    ENB = GPIO.PWM(38, 100)
    ENA.start(0)
    ENB.start(0)
    
    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(31, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)
def reset():
    #GPIO.output(36, GPIO.LOW)
    #GPIO.output(38, GPIO.LOW)
    #ENA.stop()
    #ENB.stop()
    
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    ENA.ChangeDutyCycle(0)
    ENB.ChangeDutyCycle(0)
def front():
    #GPIO.output(36, GPIO.HIGH)
    #GPIO.output(38, GPIO.HIGH)
    
    
    GPIO.output(29, GPIO.HIGH)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.LOW)
    ENA.ChangeDutyCycle(40)
    ENB.ChangeDutyCycle(40)
    
def back():
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.HIGH)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.HIGH)
    ENA.ChangeDutyCycle(40)
    ENB.ChangeDutyCycle(40)
    
def left():
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.HIGH)
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.LOW)
    ENA.ChangeDutyCycle(40)
    ENB.ChangeDutyCycle(40)
    
def right():
    GPIO.output(29, GPIO.HIGH)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.HIGH)
    ENA.ChangeDutyCycle(40)
    ENB.ChangeDutyCycle(40)


if __name__ == "__main__":
    GPIO.cleanup()
    init()
    reset()
        
    client = mqtt.Client(clientid)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, password)

    print('Connecting to broker: ' + broker)
    client.connect(broker, port)
    

    client.loop_forever()

    #
    GPIO.cleanup()

