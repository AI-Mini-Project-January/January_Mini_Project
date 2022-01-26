# Generated by Django 2.2.5 on 2022-01-25 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClimateMessage',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('temperature', models.FloatField()),
                ('rain', models.IntegerField()),
                ('cloth', models.TextField()),
            ],
            options={
                'db_table': 'ClimateMessage',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_identi', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('age', models.IntegerField()),
                ('profile_img', models.TextField()),
            ],
            options={
                'db_table': 'User',
                'managed': False,
            },
        ),
    ]