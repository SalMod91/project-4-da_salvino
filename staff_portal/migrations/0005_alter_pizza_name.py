# Generated by Django 3.2.23 on 2024-01-18 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_portal', '0004_alter_pizza_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
