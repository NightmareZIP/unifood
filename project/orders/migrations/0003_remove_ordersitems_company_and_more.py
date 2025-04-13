# Generated by Django 4.2 on 2025-04-12 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0003_menu_address"),
        ("orders", "0002_orders_created_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ordersitems",
            name="company",
        ),
        migrations.RemoveField(
            model_name="ordersitems",
            name="customer_comment",
        ),
        migrations.RemoveField(
            model_name="ordersitems",
            name="customer_name",
        ),
        migrations.RemoveField(
            model_name="ordersitems",
            name="custumer_phone",
        ),
        migrations.RemoveField(
            model_name="ordersitems",
            name="status",
        ),
        migrations.AddField(
            model_name="orders",
            name="customer_comment",
            field=models.TextField(
                blank=True, null=True, verbose_name="Комментарий покупателя"
            ),
        ),
        migrations.AddField(
            model_name="orders",
            name="customer_name",
            field=models.CharField(
                default="Name", max_length=255, verbose_name="Имя покупателя"
            ),
        ),
        migrations.AddField(
            model_name="orders",
            name="custumer_phone",
            field=models.CharField(
                default="+79999999999",
                max_length=255,
                verbose_name="Телефон покупателя",
            ),
        ),
        migrations.AddField(
            model_name="orders",
            name="items",
            field=models.ManyToManyField(
                through="orders.OrdersItems", to="menu.menuitem"
            ),
        ),
        migrations.AddField(
            model_name="orders",
            name="menu",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="menu.menu",
                verbose_name="Меню",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="orders",
            name="owner_comment",
            field=models.TextField(
                blank=True, null=True, verbose_name="Комментарий покупателя"
            ),
        ),
        migrations.AddField(
            model_name="orders",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "New order"),
                    ("ready", "Ready for delivery"),
                    ("delivered", "Delivered"),
                    ("cancelled", "Cancelled"),
                    ("rejected", "Rejected"),
                ],
                default="new",
            ),
        ),
        migrations.AddField(
            model_name="orders",
            name="total_cost",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ordersitems",
            name="order",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.orders",
                verbose_name="Заказ",
            ),
            preserve_default=False,
        ),
    ]
