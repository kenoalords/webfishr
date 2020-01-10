from allauth.account.adapter import DefaultAccountAdapter
from .tasks import send_allauth_email
from django.core.serializers import serialize, deserialize

class QueueEmailSendAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        # msg.send()
        send_allauth_email.delay(serialize('json', msg))
