# Generated by Django 2.2 on 2021-01-28 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20170910_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]