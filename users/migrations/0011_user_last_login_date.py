# Generated by Django 2.2.5 on 2020-05-05 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_continuous_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
