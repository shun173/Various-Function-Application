# Generated by Django 2.2.5 on 2020-05-01 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snsapp', '0003_auto_20200501_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ecapp.Product'),
        ),
    ]
