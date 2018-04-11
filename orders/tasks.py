from celery import Celery
from django.core.mail import send_mail

from .models import Order

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def order_created(order_id):
    """
    Sending Email Sales Message
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = 'Заказ с номером {}'.format(order_id)
    message = 'Дорогой, {}, вы успешно сделали заказ. Номер вашего заказа {}'.format(order.first_name, order_id)
    mail_send = send_mail(subject, message, 'admin@takinado.su', [order.email])
    return mail_send
