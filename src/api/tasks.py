from __future__ import absolute_import, unicode_literals
from celery import shared_task

from api.helpers.send_emails import send_account_email


@shared_task
def send_account_email_task(
        request_data, host, protocol_secure, subject, path, template):
    send_account_email(request_data, host,
                       protocol_secure, subject, path, template)
