# Generated by Django 4.2 on 2025-04-18 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_ordersitems_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordersitems",
            name="uuid",
            field=models.UUIDField(auto_created=True, default=2),
            preserve_default=False,
        ),
    ]
