# Generated by Django 4.0.1 on 2022-03-11 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_auctionphotos_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.DeleteModel(
            name='AuctionPhotos',
        ),
    ]
