# Generated by Django 3.2.7 on 2021-11-14 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20211112_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliers',
            name='inn',
            field=models.CharField(db_index=True, max_length=20, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='visits',
            name='time_start',
            field=models.TimeField(verbose_name='Время начала посещения'),
        ),
    ]