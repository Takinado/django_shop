from django.conf import settings
from django.shortcuts import get_object_or_404
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


valid_ipn_received.connect(payment_notification)
