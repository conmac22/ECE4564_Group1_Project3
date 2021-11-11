from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import serviceKeys
import requests
import pymongo

# Object instances set-up
app = Flask(__name__)
auth = HTTPBasicAuth()

# Download Canvas file
@app.route('/Canvas', methods=['GET'])
@auth.login_required
def download_file():
    file = request.args.get('file')
    response = requests.get('https://vt.instructure/api/v1/4564/files/{}?access_token={}'.format(file, serviceKeys.canvasToken))
    # Not working ^
    return response.json()

# Control LED
@app.route('/LED', methods = ['GET'])
@auth.login_required
def control_led():
    command = request.args.get('command=')
    # Split command into arguments for request
    # Send request (zeronfig listen)

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
    app.run()