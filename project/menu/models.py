#подключаем библиотеки
from datetime import datetime
from django.db import models
from company.models import Company
from helper.images import upload_to
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
class Menu(models.Model):
    """Сущноcть компании

    Args:
        массив аргументов сущности

    Returns:
        Объект Model
    """
    #создание аргумента сущности
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='menus')
    image = models.ImageField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        """_summary_

        Returns:
            string: наименование экземпляра в сущности для админ панели
        """
        return '%s' % self.name


class MenuItem(models.Model):
    """Сущноcть блюда

    Args:
        массив аргументов сущности

    Returns:
        Объект Model
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='dishes')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    discount = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True, default='Другое')
    
    def __str__(self):
        """_summary_

        Returns:
            string: наименование экземпляра в сущности для админ панели
        """
        return '%s' % self.name
    
    @property
    def discount_price(self):
        is_dicount = self.discount
        started = self.discount_start is None or self.discount_start<=timezone.now()
        not_ended = self.discount_end is None or self.discount_end>=timezone.now()
        if is_dicount and started and not_ended:
            return round(self.price - (self.price * is_dicount)/100,2)
        else:
            return self.price
            
         