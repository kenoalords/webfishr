# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render, reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.serializers import serialize, deserialize

from fishr.models import Order

SITE = Site.objects.get_current()

@shared_task
def send_subscription_email(email, uuid):
    email_body = render_to_string('email/subscription_notification.html', context={ 'uuid': uuid, 'current_site': SITE })
    link = "{0}{1}".format(SITE.domain, reverse('email_verify', kwargs={ 'uuid': uuid }))
    site_name = "{0} Team".format(SITE.name)
    email_body_text = """
                    Hello,

                    Thank you for joining our awesome mailing list.
                    Please copy and paste the link below into your browser to activate your subscription.

                    {0}

                    BR.
                    {1}
                    """
    text = email_body_text.format(link, site_name)
    email = EmailMultiAlternatives(
                    to=[email,],
                    subject='Complete your newsletter subscription!',
                    body= text
                )
    email.attach_alternative(email_body, 'text/html')
    email.send()


# Order notification
@shared_task
def send_order_notification(email, pk):
    order = Order.objects.get(uuid=uuid)
    link = "{0}{1}".format(SITE.domain, reverse('order', kwargs={ 'pk': pk }))
    email_body = render_to_string('email/order_notification.html', context={ 'uuid': uuid, 'current_site': SITE, 'order': order, 'link': link })
    site_name = "{0} Team".format(SITE.name)
    email_body_text = """
                    Hello {},

                    Your order was successful.
                    You are just one step away from enjoying our professional online services.

                    Your order details are as follows;
                    Package: {} Package
                    Amount: N{}

                    Please copy and paste the link below into your browser to make payment using your preferred payment method.
                    {}

                    BR.
                    {}
                    """
    text = email_body_text.format(order.user.first_name, order.package.title, int(order.amount), link, site_name)
    email = EmailMultiAlternatives(
                    to=[email,],
                    subject='Hello %s, View Your Order Details' % order.user.first_name.capitalize(),
                    body= text
                )
    email.attach_alternative(email_body, 'text/html')
    email.send()

    admin_email_body = """
                            Hello Admin,

                            %s placed an order for %s package
                            Order Amount: N%s

                            Thank you
                        """
    admin_body = admin_email_body % ( order.user.first_name, order.package.title, int(order.amount) )
    admin_email = EmailMessage(to=['web@webfishr.com', 'kenoalords@gmail.com'], subject='New order from %s' % order.user.first_name, body=admin_body)
    admin_email.send()

@shared_task
def send_order_payment_notification(uuid):
    order = Order.objects.get(uuid=uuid)
    email_body = render_to_string('email/order_complete.html', context={ 'uuid': uuid, 'current_site': SITE, 'order': order })
    email_body_text = """
                        Hello %s,

                        Congratulation!!! Your order payment was successful.
                        Your order details are as follows;
                        Package: %s
                        Theme: %s
                        Domain: %s
                        Amount: N%s

                        We look forward to receiving your website information as soon as possible in other to commence your work.

                        BR.

                        %s Team
                    """
    text = email_body_text % (order.user.first_name, order.package.title, order.theme.title, order.domain_name, order.amount, SITE.name)
    email = EmailMultiAlternatives(to=[order.user.email,], subject='%s your order is complete!' % order.user.first_name, body=text)
    email.attach_alternative(email_body, 'text/html')
    email.send()
