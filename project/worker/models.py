# подключаем библиотеки
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Worker(models.Model):
    """Класс для создания и работы с сущностью Работника компании

    Args:
        Поля модели

    Returns:
        Model object: обхект для манипуляций с сущностью
    """
    # Пример создания поля
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)  # фамилия
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Телефон формата: '+999999999'.")
    contact_phone = models.CharField(
        validators=[phone_regex], max_length=12, unique=True)
    country = models.CharField(max_length=255)
    user_id = models.OneToOneField(
        User, related_name='worker_user', on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True)
    head = models.ForeignKey(
        'self', related_name='worker', on_delete=models.CASCADE, null=True, blank=True)
    # Пример создания внешнего ключа компании
    company = models.ForeignKey(
        'company.Company', related_name='company', on_delete=models.CASCADE, null=True, blank=True)
    is_head = models.BooleanField(default=False)

    def __str__(self):
        """Отображение названия записи сущности в админ панели

        Returns:
            string: Название компании
        """
        return '%s' % self.name
