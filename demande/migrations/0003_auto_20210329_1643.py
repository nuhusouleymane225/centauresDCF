# Generated by Django 3.1.7 on 2021-03-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demande', '0002_demande_a_rembourser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='date_frais',
            field=models.DateTimeField(null=True, verbose_name='Date de frais'),
        ),
    ]
