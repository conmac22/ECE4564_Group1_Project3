from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from zeroconf import ServiceBrowser, Zeroconf
from threading import Thread
import serviceKeys
import requests
import pymongo
import urllib.request

# Zeroconf listener
class ZeroconfListener:
    def add_service(self, zeroconf, type, name):
        global ipAddress, port, ledColors
        info = zeroconf.get_service_info(type, name)
        ipAddress = info.parsed_addresses()[0]
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
@app.route('/Canvas', methods=['GET', 'POST'])
@auth.login_required
def canvas_file():
    operation = request.args.get('operation')
    filename = request.args.get('file')
    courseId = '136283'
    
    if operation == 'download':
        response = requests.get('https://vt.instructure.com/api/v1/courses/{}/files/?access_token={}&search_term={}'.format(courseId, serviceKeys.canvasToken, filename))
        urllib.request.urlretrieve(response.json()[0]['url'], filename)
        return response.text
    if operation == 'upload':
        stepOneParams = {'name':filename}
        firstResponse = requests.post('https://vt.instructure.com/api/v1/users/self/files/?access_token={}'.format(serviceKeys.canvasToken), data=stepOneParams)
        print(firstResponse.text)
        uploadUrl = firstResponse.json()['upload_url']
        uploadParams = firstResponse.json()['upload_params']
        uploadParams['file'] = '@'+filename
        print(uploadParams)
        secondResponse = requests.post(uploadUrl, data=uploadParams)
        return secondResponse.text
    

# Get LED status
@app.route('/LED', methods = ['GET', 'POST'])
@auth.login_required
def led():
    global ipAddress, port, ledColors
    zeroconf = Zeroconf()
    listener = ZeroconfListener()
    browser = ServiceBrowser(zeroconf, '_http._tcp.local.', listener)
    try:
        input('Press enter to exit...\n')
    finally:
        zeroconf.close()
    # GET
    if len(request.args) == 0:
        try:
            response = requests.get('http://'+str(ipAddress)+':'+str(port)+'/LED', timeout=10)
            return response.text
        except requests.exceptions.Timeout:
            return jsonify({'error': 'The LED Pi connection timed out.\n'}, 400)
        except requests.exceptions.RequestException:
            return jsonify({'error': 'The LED Pi service is not available.\n'}, 400)
    # POST
    else:
        split_commands = request.args.get('command').split('-')
        params = {'status': split_commands[0], 'color': split_commands[1], 'intensity': split_commands[2]}
        if split_commands[1] not in ledColors:
            return jsonify({'The specified color is not available.\n'}, 400)
        else:
            response = requests.post('http://'+str(ipAddress)+':'+str(port)+'/LED', data=params)
            return response.text

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
    return jsonify({'error': 'Could not verify your access level for that URL. You have to login with proper credentials.\n'}, 401)


if __name__ == '__main__':
    global ipAddress, port, ledColors
    ipAddress = ''
    port = ''
    ledColors = []
    app.run(host='0.0.0.0')