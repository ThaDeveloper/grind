import jwt
from datetime import datetime, timedelta

from django.conf import settings

def generate_simple_token(email):
    """
    Generates a JSON Web Token
    """
    dt = datetime.now() + timedelta(days=2)

    token = jwt.encode({
        'email': email,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')
