
from datetime import timedelta, datetime
from flask import jsonify
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from app.utils.utils import encode_handler
from app.models.user import User
from database.users_db import UsersDB
from app.views.users import users_view
from app.views.redflags import redflags_view
from app.views.media import media


db = UsersDB()
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'joel@Da4!'
app.config['JWT_AUTH_URL_RULE'] = '/ireporter/api/v2/auth/login'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=10)

def authenticate(username, password):
    users = db.login(username, password)
    if users and users != 'False':
            user=User(**users)
            user.id = users['userid']
            user.isAdmin = users['is_admin']
            print(users)
            app.config['JWT_SECRET_KEY'] = str(users['userid'])+str(datetime.now())
            return user

def identity(payload):
    user = db.check_id(payload['identity'])
    if user and user != 'False':
            return user

flask_jwt = JWT(app, authenticate, identity)

from app.views import error_handlers

app.register_blueprint(users_view)
app.register_blueprint(redflags_view)
app.register_blueprint(media)

#index route
@app.route('/')
def home():
    """ home route """
    
    return jsonify({"status":200,
                            "data":[{
                                "message":"Welcome"
                            }]}), 200


@flask_jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                        'status': 200, 
                        'data' : [{
                            'token' : access_token.decode('utf-8'),
                            'user': identity.__dict__
                        }]
                   })

@flask_jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
                       'error': error.description,
                       'status': error.status_code
                   }), error.status_code

@flask_jwt.jwt_encode_handler
def customized_encode_handler(identity):
    secret = app.config['JWT_SECRET_KEY']
    algorithm = app.config['JWT_ALGORITHM']

    return encode_handler(identity, secret, algorithm)


@app.route('/ireporter/api/v2/logout')
@jwt_required()
def logout():

    app.config['JWT_SECRET_KEY'] = str(current_identity['userid'])+str(datetime.now())

    return jsonify ({
        'message': 'successfully logged out'
    }), 200  
