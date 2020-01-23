from datetime import datetime, timedelta
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from api.authentication.backends import GrindJWTAuthentication
from api.models import User
from api.helpers.jwt import generate_simple_token


def account_url_metadata(data, host, protocol_secure):
    token = generate_simple_token(data.get('email'))
    if protocol_secure:
        protocol = "https://"
    else:
        protocol = "http://"
    uid = urlsafe_base64_encode(force_bytes(
        data.get('email')))
    time = datetime.now()
    time = datetime.strftime(time, '%d-%B-%Y %H:%M')

    return (token, host, protocol, uid, time)
