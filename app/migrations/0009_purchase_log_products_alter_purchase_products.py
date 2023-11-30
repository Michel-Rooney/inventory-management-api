# Generated by Django 4.2.7 on 2023-11-29 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_purchase_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='log_products',
            field=models.ManyToManyField(blank=True, to='app.logproduct'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(to='app.product'),
        ),
    ]
