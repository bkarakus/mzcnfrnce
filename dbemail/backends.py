from django.core.mail import get_connection
from django.core.mail.backends.base import BaseEmailBackend

from .conf import settings
from .models import EmailLog


class EmailBackend(BaseEmailBackend):

    """Wrapper email backend that records all emails in a database model"""

    def __init__(self, **kwargs):
        super(EmailBackend, self).__init__(**kwargs)
        self.connection = get_connection(settings.EMAIL_LOG_BACKEND, **kwargs)

    def send_messages(self, email_messages):
        num_sent = 0
        for message in email_messages:
            to = '; '.join(message.to)
            cc = '; '.join(message.cc)
            bcc = '; '.join(message.bcc)
            recipients = 'to: %s | cc: %s | bcc: %s' % (to, cc, bcc)
            email = EmailLog.objects.create(
                from_email=message.from_email,
                recipients=recipients,
                subject=message.subject,
                body=message.body,
            )
            message.connection = self.connection
            num_sent += message.send()
            if num_sent > 0:
                email.ok = True
                email.save()
        return num_sent