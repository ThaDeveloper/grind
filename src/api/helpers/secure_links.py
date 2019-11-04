from datetime import datetime, timedelta
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from api.authentication.backends import GrindJWTAuthentication
from api.models import User
from api.helpers.jwt import generate_simple_token


def account_url_metadata(request):
    token = generate_simple_token(request.data['email'])
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = request.META['SERVER_PROTOCOL'][:4]
    uid = urlsafe_base64_encode(force_bytes(
            request.data['username']))
    time = datetime.now()
    time = datetime.strftime(time, '%d-%B-%Y %H:%M')

    return (token, domain, protocol, uid, time)
