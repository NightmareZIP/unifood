#подключаем библиотеки
from django.db import models
from company.models import Company
from menu.models import MenuItem, Menu
class Orders(models.Model):
    """Сущноcть компании

    Args:
        массив аргументов сущности

    Returns:
        Объект Model
    """
    class  StatusEnum(models.TextChoices):
        NEW = "new", "New order"
        READY = "ready", "Ready for delivery"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        REJECTED = "rejected", "Rejected"
        

    #создание аргумента сущности
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, verbose_name="Компания")
    status = models.CharField(choices=StatusEnum.choices, default=StatusEnum.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False, verbose_name="Меню")
    customer_name = models.CharField(max_length=255, default="Name", verbose_name="Имя покупателя")
    #TODO regex pattern
    custumer_phone = models.CharField(max_length=255, default="+79999999999", verbose_name="Телефон покупателя")
    customer_comment = models.TextField(blank=True, null=True, verbose_name="Комментарий покупателя")
    owner_comment = models.TextField(blank=True, null=True, verbose_name="Комментарий покупателя")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    menu_items = models.ManyToManyField(MenuItem, through="OrdersItems")
    uuid = models.UUIDField(auto_created=True)

    def __str__(self):
        """_summary_

        Returns:
            string: наименование экземпляра в сущности для админ панели
        """
        return '%s' % self.id

class OrdersItems(models.Model):
    """Сущноcть компании

    Args:
        массив аргументов сущности

    Returns:
        Объект Model
    """
    
    #создание аргумента сущности
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=False, verbose_name="Заказ")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=False, verbose_name="Пункт меню")
    amount = models.IntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2)
   
    def __str__(self):
        """_summary_

        Returns:
            string: наименование экземпляра в сущности для админ панели
        """
        return f'{self.id}:{self.menu_item.name}'

