from typing import Tuple
from bluetooth import *   #bluetooth
import RPi.GPIO as GPIO
import time

#GPIO
GPIO.setmode(GPIO.BCM)

ServoPin = 17
SERVO_MIN_DUTY = 3
SERVO_MAX_DUTY = 12
cur_pos = 90

GPIO.setup(ServoPin,GPIO.OUT)
servo = GPIO.PWM(ServoPin, 50)
servo.start(0)

#servo
def servo_control(degree,delay):
    if degree > 180:
        degree = 180
    duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY - SERVO_MIN_DUTY)/180.0)
         #print("Degree : {} to {} (Duty)".format(degree, duty))
    servo.ChangeDutyCycle(duty)
    time.sleep(delay)
    servo.ChangeDutyCycle(0)


while True:
    #bluetooth
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]
    uuid = "00001801-0000-1000-8000-00805f9b34fb"
    advertise_service( server_sock, "SampleServer",
                    service_id = uuid,
                    service_classes = [ uuid, SERIAL_PORT_CLASS ],
                    profiles = [ SERIAL_PORT_PROFILE ], 
    #                   protocols = [ OBEX_UUID ] 
                        )
                    
    print("Waiting for connection on RFCOMM channel %d" % port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)
    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) == 0: break
            print("received [%s]" % data)
            control_data = data.decode()
            if control_data == '2':            
                cur_pos = cur_pos + 10
                if cur_pos >= 180:
                    cur_pos = 180
            elif control_data == '3':
                cur_pos = cur_pos - 10
                if cur_pos <= 0:
                    cur_pos = 0
            servo_control(cur_pos,0.1)
            
            
    except IOError:
        pass
    print("disconnected")
    client_sock.close()
    server_sock.close()
    print("all done")
