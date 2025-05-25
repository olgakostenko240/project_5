import os

from celery import Celery

# Установите модуль настроек Django по умолчанию для программы «celery»
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузить модули задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()
