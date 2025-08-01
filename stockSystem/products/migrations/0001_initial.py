# Generated by Django 5.2.4 on 2025-07-28 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Nombre del producto')),
                ('description', models.CharField(max_length=500, verbose_name='Detalle técnico')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio')),
                ('stock', models.IntegerField(verbose_name='Stock total')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Nombre del proveedor')),
                ('country', models.CharField(max_length=200, verbose_name='País de origen')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='ProductSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio del proveedor')),
                ('supplier_stock', models.IntegerField(verbose_name='Stock del proveedor')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Producto')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.supplier', verbose_name='Proveedor')),
            ],
            options={
                'verbose_name': 'Producto por proveedor',
                'verbose_name_plural': 'Productos por proveedor',
                'unique_together': {('product', 'supplier')},
            },
        ),
    ]
