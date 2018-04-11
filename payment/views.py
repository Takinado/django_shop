from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from orders.models import Order


def payment_process(request):
    """
    https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
    :param request:
    :return:
    """
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    # host = request.get_host()

    # What you want the button to do.
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
        'item_name': 'Заказ {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        # 'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        # 'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        # 'cancel_url': 'http://{}{}'.format(host, reverse('payment:canceled')),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done')),
        "cancel_return": request.build_absolute_uri(reverse('payment:canceled')),

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        'order': order,
        'form': form,
    }
    return render(request, 'payment/process.html', context)


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
