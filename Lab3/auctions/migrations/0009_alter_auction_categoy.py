# Generated by Django 4.0.4 on 2022-06-24 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auction_categoy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='categoy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
        ),
    ]
