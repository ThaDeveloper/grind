import os

from django.template.loader import render_to_string
from django.core.mail import send_mail

from api.helpers.secure_links import account_url_metadata
from api.models import User


def send_account_email(data, host, protocol_secure, subject, path, template):
    token, host, protocol, uid, time = account_url_metadata(
        data, host, protocol_secure)
    email = data.get('email')
    first_name = data.get('first_name')
    message = render_to_string(
        template, {
            'domain': host,
            'uid': uid,
            'token': token,
            'name': first_name,
            'time': time,
            'link': protocol + host + path + uid + '/' + token
        })

    to_email = email
    from_email = os.getenv('DEFAULT_FROM_EMAIL')
    send_mail(
        subject,
        'Grind account contact',
        from_email, [
            to_email,
        ],
        html_message=message,
        fail_silently=False
    )
