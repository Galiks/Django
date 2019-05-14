# Generated by Django 2.2.1 on 2019-05-14 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('discount', models.FloatField()),
                ('label', models.CharField(max_length=10)),
                ('url', models.URLField()),
                ('image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('time', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
