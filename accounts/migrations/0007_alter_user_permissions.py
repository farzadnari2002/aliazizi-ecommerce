# Generated by Django 5.1.5 on 2025-02-03 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_userprofile_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='permissions',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
