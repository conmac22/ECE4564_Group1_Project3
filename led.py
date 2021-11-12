import RPi.GPIO as GPIO
from flask import Flask, jsonify, abort, make_response, request
from time import sleep
from zeroconf import ServiceInfo, ServiceBrowser, Zeroconf

app = Flask(__name__)

class ZeroconfBroadcast:
    
    def zeroinit():
        name = 'ledPI'
        type_ = '_UPnP._tcp.local.'
        #description = {'deviceName': name}
        zeroconf = Zeroconf()
        info = ServiceInfo(type_, name + '.' + type_)
        
        zeroconf.register_service(info)
        generate_service_broadcast(info)
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/LED', methods=['GET'])
def get_led():
    print('Test')
    status = request.args.get('status')
    color = request.args.get('color')
    intensity = int(request.args.get('intensity'))
    
    if status == 'on':
        if color == 'magenta':
            led_magenta(intensity)
        elif color == 'cyan':
            led_cyan(intensity)
        elif color == 'yellow':
            led_yellow(intensity)
        elif color == 'white':
            led_white(intensity)
        elif color == 'red':
            led_red(intensity)
        elif color == 'green':
            led_green(intensity)
        elif color == 'blue':
            led_blue(intensity)
        else:
            abort(404)
    elif status == 'off':
        color(0, 0, 0)


def color(r, g, b):
    red.ChangeDutyCycle(r)
    green.ChangeDutyCycle(g)
    blue.ChangeDutyCycle(b)

def led_magenta(intensity):
    # led.color(1, 0, 1)
    color(intensity, 0, intensity)
    print("Turned on magenta")
    sleep(1)

def led_cyan(intensity):
    # led.color(0,1,1)
    color(0, intensity, intensity)
    print("Turned on cyan")
    sleep(1)

def led_yellow(intensity):
    # led.color(1,1,0)
    color(intensity, intensity, 0)
    print("Turned on yellow")
    sleep(1)


def led_white(intensity):
    # led.color(1,1,1)
    color(intensity, intensity, intensity)
    print("Turned on white")
    sleep(1)


def led_red(intensity):
    # led.color(1,0,0)
    color(intensity, 0, 0)
    print("Turned on red")
    sleep(1)


def led_green(intensity):
    # led.color(0,1,0)
    color(0, intensity, 0)
    print("turned on green")
    sleep(1)

def led_blue(intensity):
    # led.color(0,0,1)
    color(0, 0, intensity)
    print("turned on blue")
    sleep(1)


if __name__ == "__main__":

    # setup RGBLED
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    
    global red, green, blue
    red = GPIO.PWM(16, 100)
    green = GPIO.PWM(20, 100)
    blue = GPIO.PWM(21, 100)
    red.start(0)
    green.start(0)
    blue.start(0)

    # Run Flask
    blah = ZeroconfBroadcast
    blah.zeroinit()
    app.run(host='0.0.0.0')
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        red.stop()
        green.stop()
        blue.stop()
        GPIO.cleanup()
