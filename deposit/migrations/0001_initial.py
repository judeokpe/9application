# Generated by Django 4.2.4 on 2024-04-10 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=5, max_digits=20)),
                ('wallet_type', models.CharField(choices=[('BTC', 'Bitcoin'), ('LTC', 'Litecoin'), ('USDT', 'Tether'), ('BNB', 'Binance'), ('ETH', 'Ethereum')], max_length=10)),
                ('wallet_address', models.CharField(max_length=100)),
                ('naira_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=20)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
