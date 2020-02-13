from LPapp import app
from LPapp.models import *
from LPapp.MyFunctions import *

# external
from flask import (
    Flask,
    request,
    jsonify,
    make_response,
)
from flask_cors import cross_origin
from LPapp import bcrypt

@app.route("/")
def test_route():
    return "working"

# user signup
@app.route('/user/signup', methods=['POST'])
@cross_origin(supports_credentials=True)
def user_signup():

    username=request.json['username']
    password = request.json['password']
    password = bcrypt.generate_password_hash(password).decode() # hashed, better than SHA1
    email=request.json['email']

    email_check = Users.query.filter_by(email=email).first()

    if email_check:
        payLoad = {
            'username':'',
            'password':'',
            'email':'',
            'admin_status':0,
            'pro_status':0,
            'total_coin':0,
            'current_coin':0,
            'spent_coin':0,
            'jwt':'',
            'status':'User-Already-Exsists'
        }
        return make_response(jsonify(payLoad), 208)

    new_user = Users(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    user = Users.query.filter_by(email=request.json['email']).first()
    auth_token = encode_auth_token(user.id)

    try:
        TokenValue = auth_token.decode()
    except Exception as e: # TypeError object has no attribute Token
        payLoad = {
        'username':username,
        'password':password,
        'email':email,
        'admin_status':0,
        'pro_status':0,
        'total_coin':0,
        'current_coin':0,
        'spent_coin':0,
        'jwt':'',
        'status':"Failed-to-generate-Token"
        }
        return make_response(jsonify(payLoad), 500)

    payLoad = {
        'username':username,
        'password':password,
        'email':email,
        'admin_status':0,
        'pro_status':0,
        'total_coin':0,
        'current_coin':0,
        'spent_coin':0,
        'jwt':TokenValue,
        'status':"User-Created-Successfully"
    }
    return make_response(jsonify(payLoad), 200)


# user login
@app.route('/user/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def user_login():

    email=request.json['email']
    password=request.json['password']

    email_exsist = Users.query.filter_by(email=email).first()

    try:
        if email_exsist==None:
            payLoad = {
                'status': 'fail',
                'message': 'User-does-not-exsist',
                'auth_token':'',
                'admin_status':0
            }
            return make_response(jsonify(payLoad), 404)

        user = Users.query.filter_by(email=request.json['email']).first()

        if bcrypt.check_password_hash(user.password, password):   #password == user.password
            auth_token = encode_auth_token(user.id)
            admin_status_ = Users.query.filter_by(email=email).first().admin_status
            payLoad = {
                'status':'success',
                'message':'Successfully-logged-in',
                'auth_token':auth_token.decode(),
                'admin_status':admin_status_
            }
            return make_response(jsonify(payLoad), 200)
        else:
            payLoad = {
                'status': 'fail',
                'message': 'Wrong-Credentials! Check-Again.',
                'auth_token':'',
                'admin_status':0
            }
            return make_response(jsonify(payLoad), 401)
    except Exception as e:
        payLoad = {
            'status': 'fail',
            'message': 'Wrong-Credentials! Check-Again.',
            'auth_token':'',
            'admin_status':0
        }
        return make_response(jsonify(payLoad), 401)