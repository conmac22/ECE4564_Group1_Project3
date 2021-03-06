import RPi.GPIO as GPIO
from flask import Flask, jsonify, abort, make_response, request
from zeroconf import ServiceInfo, ServiceBrowser, Zeroconf
import socket
app = Flask(__name__)


class ZeroconfBroadcast:
    
    def init():
        name = 'ledPI'
        type_ = '_http._tcp.local.'
        properties_ = {'colors': ['red','blue','green','magenta','yellow','white','cyan']}
        zeroconf = Zeroconf()
        info = ServiceInfo(type_, name + '.' + type_,
                           addresses=[socket.inet_aton("172.20.10.10")],
                           port=5000, properties=properties_)
        
        zeroconf.register_service(info)
        
        #generate_service_broadcast(info)
        
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    

@app.route('/LED', methods=['GET', 'POST'])
def led():
    # Setup RPi global variables
    global status, color
    
    if request.method == 'GET':
        return make_response(jsonify({'status': status, 'color': color}), 200)
    elif request.method == 'POST':
        status = request.form.get('status')
        color = request.form.get('color')
        intensity = int(request.form.get('intensity'))
        
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
            duty_cycle(0, 0, 0)
        return make_response(jsonify({'success': 'True'}), 200)
    else:
        abort(404)


def duty_cycle(r, g, b):
    red.ChangeDutyCycle(r)
    green.ChangeDutyCycle(g)
    blue.ChangeDutyCycle(b)

def led_magenta(intensity):
    # led.color(1, 0, 1)
    duty_cycle(intensity, 0, intensity)
    print("Turned on magenta")

def led_cyan(intensity):
    # led.color(0,1,1)
    duty_cycle(0, intensity, intensity)
    print("Turned on cyan")

def led_yellow(intensity):
    # led.color(1,1,0)
    duty_cycle(intensity, intensity, 0)
    print("Turned on yellow")


def led_white(intensity):
    # led.color(1,1,1)
    duty_cycle(intensity, intensity, intensity)
    print("Turned on white")


def led_red(intensity):
    # led.color(1,0,0)
    duty_cycle(intensity, 0, 0)
    print("Turned on red")
 
def led_green(intensity):
    # led.color(0,1,0)
    duty_cycle(0, intensity, 0)
    print("turned on green")

def led_blue(intensity):
    # led.color(0,0,1)
    duty_cycle(0, 0, intensity)
    print("turned on blue")


if __name__ == "__main__":

    # Setup RGBLED
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
    zero = ZeroconfBroadcast
    zero.init()
    app.run(host='0.0.0.0')
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        red.stop()
        green.stop()
        blue.stop()
        GPIO.cleanup()
