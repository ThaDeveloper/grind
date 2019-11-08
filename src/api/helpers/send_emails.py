import os 

from django.template.loader import render_to_string
from django.core.mail import send_mail

from api.helpers.secure_links import account_url_metadata
from api.models import User


def send_account_email(request, subject, path, template):
    token, domain, protocol, uid, time = account_url_metadata(request)
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    message = render_to_string(
        template, {
            'domain': domain,
            'uid': uid,
            'token': token,
            'name': user.first_name,
            'time': time,
            'link': protocol + domain + path + uid + '/' + token
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
