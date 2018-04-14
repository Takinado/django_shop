import os
from io import BytesIO

import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from orders.models import Order


def payment_notification(sender, **kwargs):
    """
    https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
    :param sender:
    :param kwargs:
    :return:
    """
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        # Undertake some action depending upon `ipn_obj`.
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()

        # PDF Generation
        html = render_to_string('orders/order_pdf.html', {'order': order})
        out = BytesIO()
        weasyprint.HTML(string=html).write_pdf(
            out,
            stylesheets=[weasyprint.CSS(os.path.join(settings.STATIC_ROOT, 'css/bootstrap.css'))],
        )

        # Sending email
        subject = 'Онлайн магазин - заказ: {}'.format(order.id)
        message = 'К email сообщению приклеплён PDF-файл с информацией о заказе.'
        email = EmailMessage(subject, message, 'takinado@mail.ru', [order.email])
        email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
        email.send()


valid_ipn_received.connect(payment_notification)
