from datetime import datetime, timedelta
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from api.authentication.backends import GrindJWTAuthentication
from api.models import User
from api.helpers.jwt import generate_simple_token


def account_url_metadata(request):
    token = generate_simple_token(request.data.get('email'))
    domain = request.get_host()
    if request.is_secure():
            protocol = "https://"
    else:
            protocol = "http://"
    uid = urlsafe_base64_encode(force_bytes(
            request.data.get('email')))
    time = datetime.now()
    time = datetime.strftime(time, '%d-%B-%Y %H:%M')

    return (token, domain, protocol, uid, time)
