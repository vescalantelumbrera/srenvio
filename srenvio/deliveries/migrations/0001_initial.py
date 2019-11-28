# Generated by Django 2.2.7 on 2019-11-27 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_number', models.CharField(default='', max_length=20, unique=True)),
                ('carrier', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'delivery',
            },
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.DecimalField(decimal_places=4, max_digits=9)),
                ('width', models.DecimalField(decimal_places=4, max_digits=9)),
                ('height', models.DecimalField(decimal_places=4, max_digits=9)),
                ('weight', models.DecimalField(decimal_places=4, max_digits=9)),
                ('real_length', models.DecimalField(decimal_places=4, max_digits=9)),
                ('real_width', models.DecimalField(decimal_places=4, max_digits=9)),
                ('real_height', models.DecimalField(decimal_places=4, max_digits=9)),
                ('real_weight', models.DecimalField(decimal_places=4, max_digits=9)),
                ('total_weight', models.DecimalField(decimal_places=4, max_digits=9)),
                ('over_weight', models.IntegerField()),
                ('delivery', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='deliveries.Delivery')),
            ],
            options={
                'db_table': 'parcel',
            },
        ),
    ]
