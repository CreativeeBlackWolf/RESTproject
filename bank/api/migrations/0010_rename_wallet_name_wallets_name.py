# Generated by Django 4.0.3 on 2022-04-02 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_transactions_payment_alter_transactions_wallet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallets',
            old_name='wallet_name',
            new_name='name',
        ),
    ]
