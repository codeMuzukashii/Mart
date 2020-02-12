# Generated by Django 3.0.3 on 2020-02-10 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('stock_pcs', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('shop_id', models.CharField(max_length=5, null=True)),
                ('vip', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('shop_id', models.CharField(max_length=5, null=True)),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='urmart.Product')),
            ],
            options={
                'db_table': 'order',
            },
        ),
    ]