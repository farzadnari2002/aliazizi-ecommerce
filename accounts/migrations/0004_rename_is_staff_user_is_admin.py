# Generated by Django 5.1.5 on 2025-01-26 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_permissions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_staff',
            new_name='is_admin',
        ),
    ]
