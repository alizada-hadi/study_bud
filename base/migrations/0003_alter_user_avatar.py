# Generated by Django 3.2.7 on 2021-10-08 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20211008_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='images/avatar.svg', null=True, upload_to='avatar/'),
        ),
    ]