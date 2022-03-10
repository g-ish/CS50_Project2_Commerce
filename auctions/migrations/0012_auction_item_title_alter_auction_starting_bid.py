# Generated by Django 4.0.1 on 2022-02-23 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auction_starting_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='item_title',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auction',
            name='starting_bid',
            field=models.FloatField(),
        ),
    ]
