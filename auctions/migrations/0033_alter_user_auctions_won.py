# Generated by Django 4.0.1 on 2022-09-15 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0032_user_auctions_won'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auctions_won',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auctions_won', to='auctions.auction'),
        ),
    ]
