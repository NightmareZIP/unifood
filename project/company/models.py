#подключаем библиотеки
from django.db import models
from django.core.validators import RegexValidator
from tarif.models import Tarif
from helper.images import upload_to
class Company(models.Model):
    """Сущноcть компании

    Args:
        массив аргументов сущности

    Returns:
        Объект Model
    """
    #создание аргумента сущности
    name = models.CharField(max_length=255, unique=True)
    inn = models.CharField(max_length=255, blank=False, null=False)
    country = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Телефон формата: '+999999999'.")
    contact_phone = models.CharField(
        validators=[phone_regex], unique=True, max_length=12, blank=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tarif = models.ForeignKey(Tarif, null=True, blank=True, on_delete=models.CASCADE)
    tarif_date = models.DateTimeField(auto_now_add=False,  null=True, blank=True,)
    description = models.TextField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    
    def __str__(self):
        """_summary_

        Returns:
            string: наименование экземпляра в сущности для админ панели
        """
        return '%s' % self.name
