# Generated by Django 3.1.5 on 2021-01-30 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stcok',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=50, verbose_name='Download key')),
                ('name', models.CharField(max_length=50, verbose_name='Stock name')),
            ],
        ),
    ]