# Generated by Django 3.0.1 on 2020-01-06 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fishr', '0009_auto_20200106_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='expiry',
            field=models.DateField(blank=True, null=True),
        ),
    ]
