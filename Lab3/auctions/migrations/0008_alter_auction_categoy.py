# Generated by Django 4.0.4 on 2022-06-24 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auction_author_alter_auction_categoy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='categoy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
        ),
    ]