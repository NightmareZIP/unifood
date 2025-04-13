#подключаем библиотеки
from django.db import models


class Tarif(models.Model):
    """Сщноycть тарифа

    Args:
        массив аргументов сущности

    Returns:
        Объект Model
    """
    #создание аргумента сущности
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='tarifs_logo/', blank=True, null=True)
    max_workers = models.IntegerField()
    max_menu = models.IntegerField()
    max_items = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    

    def __str__(self):
        """_summary_

        Returns:
            string: наименование экземпляра в сущности для админ панели
        """
        return '%s' % self.name
