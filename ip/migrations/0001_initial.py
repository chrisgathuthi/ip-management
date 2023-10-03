# Generated by Django 4.2.5 on 2023-10-02 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.GenericIPAddressField(unique=True, verbose_name='ip address')),
                ('status', models.CharField(choices=[('reserved', 'Reserved'), ('allocated', 'Allocated'), ('available', 'Available')], max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('ip_address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ip', to='ip.ipaddress')),
            ],
        ),
    ]