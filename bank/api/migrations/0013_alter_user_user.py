# Generated by Django 4.0.3 on 2022-04-22 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_transaction_from_wallet_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user',
            field=models.CharField(max_length=128, verbose_name='Username'),
        ),
    ]