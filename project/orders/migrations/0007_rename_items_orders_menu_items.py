# Generated by Django 4.2 on 2025-04-18 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_remove_ordersitems_uuid_orders_uuid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orders",
            old_name="items",
            new_name="menu_items",
        ),
    ]
