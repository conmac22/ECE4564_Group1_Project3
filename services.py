from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import serviceKeys

# Object instances set-up
app = Flask(__name__)
auth = HTTPBasicAuth()

# This will be in MongoDB eventually
users = {
    'user1': generate_password_hash('pass1'),
    'user2': generate_password_hash('pass2'),
    'user3': generate_password_hash('pass3')
}

# Download Canvas file
@app.route('/Canvas', methods=['GET'])
@auth.login_required
def download_file():
    file = request.args.get('file')
    # Send request to Canvas

# Authentication
@auth.verify_password
def verify_password(username, password):
    if username in users and \
       check_password_hash(users.get(username), password):
        return username

# Error handling for bad username/password
@auth.error_handler
def unauthorized():
    return 'Could not verify your access level for that URL. You have to login with proper credentials.\n'


if __name__ == '__main__':
    app.run(debug=True)
    