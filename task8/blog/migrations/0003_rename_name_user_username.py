# Generated by Django 5.0 on 2023-12-24 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_user_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
    ]