# Generated by Django 3.0.3 on 2020-03-07 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20200228_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Nom du projet'),
        ),
    ]
