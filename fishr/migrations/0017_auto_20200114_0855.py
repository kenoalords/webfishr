# Generated by Django 2.2.9 on 2020-01-14 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fishr', '0016_auto_20200113_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='testimonial',
            field=models.TextField(),
        ),
    ]
