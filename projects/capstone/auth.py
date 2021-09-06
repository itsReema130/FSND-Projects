import json
from flask import request, _request_ctx_stack , abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-xudjg1cu.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000'



class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def tokenrRaise():
    raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

def authBearer():
    raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
def notFound():
    raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

def authHeader():
    raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        tokenrRaise()

    au = auth.split()
    nb = len(au)
    if au[0].lower() != 'bearer':
        authBearer()
    
    elif nb == 1:
        notFound()

    elif nb > 2:
        authHeader()

    tmp = au[1]
    return tmp
  
def authPer():
    raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

def unauth():
    raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        authPer()

    if permission not in payload['permissions']:
        unauth()
    return True

def authMal():
    raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

def token_Expired():
    raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

def invalid_Cal():
    raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience '
                               'and issuer.'
            }, 401)

def invalid_header():
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    js = json.loads(url.read())
    jwtH = jwt.get_unverified_header(token)
    opens = {}
    if 'kid' not in jwtH:
        authMal()

    for tmp in js['keys']:
        if tmp['kid'] == jwtH['kid']:
            opens = {
                'kty': tmp['kty'],
                'kid': tmp['kid'],
                'use': tmp['use'],
                'n': tmp['n'],
                'e': tmp['e']
            }

    if opens:
        try:
            payload = jwt.decode(
                token,
                opens,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            token_Expired()

        except jwt.JWTClaimsError:
            invalid_Cal()
        except Exception:
            invalid_header()
    unauth()


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator





