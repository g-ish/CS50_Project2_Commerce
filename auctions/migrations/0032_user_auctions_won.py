# Generated by Django 4.0.1 on 2022-09-15 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0031_remove_user_watch_list_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auctions_won',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auctions_won', to='auctions.auction'),
            preserve_default=False,
        ),
    ]
