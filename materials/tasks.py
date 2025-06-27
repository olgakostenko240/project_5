from datetime import timedelta
from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from materials.models import Well, Subscription
from users.models import User


@shared_task
def well_update(well_pk):
    """ Отпровляет сообщение об изменении курса """

    well = Well.objects.filter(pk=well_pk).first()
    users = User.objects.all()
    for user in users:
        subscription = Subscription.objects.filter(well=well_pk, user=user.pk).first()
        if subscription:
            send_mail(
                subject=f'Обновление курса "{well.name}"',
                message=f'Здравствуйте! Курс "{well.name}" обновился!',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )


@shared_task
def check_last_login():
    users = User.objects.filter(last_login__isnull=False)
    for user in users:
        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} отключен')
        else:
            print(f'Пользователь {user.email} активен')
