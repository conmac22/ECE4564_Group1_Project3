from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from zeroconf import ServiceBrowser, Zeroconf
from threading import Thread
import serviceKeys
import requests
import pymongo

ipAddress = ''
port = ''
ledColors = []

# Zeroconf listener
class ZeroconfListener:
    def add_service(self, zeroconf, type, name):
        print("Connected")
        info = zeroconf.get_service_info(type, name)
        ipAddress = info.parsed_addresses()
        port = info.port
        for (key, value) in info.properties.items():
            ledColors = (f'{value}')
        print(ipAddress)
        print(port)
        print(ledColors)

# Object instances set-up
app = Flask(__name__)
auth = HTTPBasicAuth()

# Download Canvas file
@app.route('/Canvas', methods=['GET'])
@auth.login_required
def download_file():
    print(request.args)
    filename = request.args.get('file')
    print(filename)
    courseId = request.args.get('course_id')
    print(courseId)
    response = requests.get('https://vt.instructure/api/v1/courses/{}/files/?access_token={}&search_term={}'.format(courseId, serviceKeys.canvasToken, filename))
    return response.json()

# Control LED
@app.route('/LED', methods = ['GET'])
@auth.login_required
def control_led():
    zeroconf = Zeroconf()
    listener = ZeroconfListener()
    argsStr = 'status=on&color=magenta&intensity=80'
    response = requests.get('http://'+ipAddress+':'+port+'/LED?' + argsStr)

def thread(zeroconf, string, listener):
    browser = ServiceBrowser(zeroconf, '_http._tcp.local.', listener)    

# Authentication
@auth.verify_password
def verify_password(username, password):
    #Connect to mongoDB
    mongoPassword = serviceKeys.mongoDbPassword
    cluster = pymongo.MongoClient('mongodb+srv://seans_laptop:' + mongoPassword + '@cluster0.kvaed.mongodb.net/Cluster0?retryWrites=true&w=majority')
    db = cluster["ECE4564_Assignment_3"]
    collection = db["service_auth"]
    
    #Verify username/password
    if collection.find_one({username:password}) != None:
        return username
    return None

# Error handling for bad username/password
@auth.error_handler
def unauthorized():
    return 'Could not verify your access level for that URL. You have to login with proper credentials.\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0')