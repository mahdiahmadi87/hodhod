# Generated by Django 5.0.1 on 2024-01-27 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0003_newsagency_news_newsagency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='newsAgency',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='newsapp.newsagency'),
        ),
    ]
