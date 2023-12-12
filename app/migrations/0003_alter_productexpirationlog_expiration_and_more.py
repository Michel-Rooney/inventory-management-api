# Generated by Django 4.2.7 on 2023-12-11 23:15

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_product_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productexpirationlog',
            name='expiration',
            field=models.DateField(validators=[app.models.validate_future_date]),
        ),
        migrations.AlterField(
            model_name='productlog',
            name='expiration',
            field=models.DateField(validators=[app.models.validate_future_date]),
        ),
    ]
