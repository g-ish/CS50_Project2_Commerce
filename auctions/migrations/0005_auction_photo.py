# Generated by Django 4.0.1 on 2022-02-22 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_comment_posteddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='photo',
            field=models.ImageField(default='Null', upload_to='auctions'),
            preserve_default=False,
        ),
    ]
