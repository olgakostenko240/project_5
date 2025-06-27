from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Well, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    CASH = "cash"
    NON_CASH = "non_cash"
    PAYMENT_METHOD = [(CASH, "cash"), (NON_CASH, "non_cash")]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Оплата",
        help_text="Укажите кто произвел оплату",
    )
    payment_date = models.DateField(verbose_name="Дата платежа", blank=True, null=True)
    payment_course = models.ForeignKey(
        Well,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        help_text="Укажите оплаченый курс",
        blank=True,
        null=True,
    )
    payment_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        help_text="Укажите оплаченый урок",
        blank=True,
        null=True,
    )
    cost = models.PositiveIntegerField(default=0, verbose_name="Стоимость покупки")
    payment_method = models.CharField(
        choices=PAYMENT_METHOD, default=CASH, verbose_name="Способ оплаты"
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="Id сессии",
        help_text="Укажите id сессии",
        blank=True,
        null=True,
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return self.payment_method
