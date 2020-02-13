from LPapp import app
from LPapp.models import *

# external
import jwt
import datetime


def debug(msg):
    print('\n\n\n'+str(msg)+'\n\n\n'+'\n\nType:\t'+str(type(msg))+'\n\n')

# JWT ENCODE/DECODE FUNCTIONS

def encode_auth_token(user_id):

    """
    Generates the Auth Token
    :param arg1: User ID
    :type arg1: Integer
    :return: JWT Token
    :rtype: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e: # Make sure secret key is set in environment, else NoneType ValueError
        debug(e)
        return e


def decode_auth_token(auth_token='auth_header'):

    """
    Decodes the auth token
    :param arg1: JWT Token
    :type arg1: String
    :return: User ID | Exception
    :rtype: Integer |  String
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


# Function that gives user id, username, email and admin_status from JWT Token

def user_info(token):

    """
    Give User Details by simplying passing JWT Token
    :param arg1: JWT Token
    :type arg1: String
    :return: User Detail | 'AuthFail'
    :rtype: Dict | String
    """
    try:
        auth_token = token.split(" ")[0]
    except: # No JWT Token in header
        return 'AuthFail'
    resp = decode_auth_token(auth_token)

    if not isinstance(resp, str):
        user = Users.query.filter_by(id=resp).first()

        try: # suppose a user is deleted, then token is valid, and thus request reaches here and then error as no id for deleted user
            return {
                'id':user.id,
                'email':user.email,
                'username':user.username,
                'admin_status':user.admin_status,
                'pro_status':user.pro_status,
                'total_coin':user.total_coin,
                'current_coin':user.current_coin,
                'spent_coin':user.spent_coin
            }
        except:
            return 'AuthFail'

    return 'AuthFail' #This should have been changed to dict type