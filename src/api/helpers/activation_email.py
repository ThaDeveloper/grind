import os 

from django.template.loader import render_to_string
from django.core.mail import send_mail

from api.helpers.secure_links import account_url_metadata

def send_activation_email(request):
    token, domain, protocol, uid, time = account_url_metadata(request)
    message = render_to_string(
        'confirm_account.html', {
            'domain': domain,
            'uid': uid,
            'token': token,
            'name': request.data['first_name'],
            'time': time,
            'link': protocol + '://' + domain + '/accounts/activate/' + uid + '/' + token
    })

    mail_subject = 'Activate your account.'
    to_email = request.data['email']
    from_email = os.getenv('DEFAULT_FROM_EMAIL')
    send_mail(
        mail_subject,
        'Verify your Account',
        from_email, [
            to_email,
        ],
        html_message=message,
        fail_silently=False
    )
