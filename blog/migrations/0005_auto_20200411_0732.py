# Generated by Django 3.0.5 on 2020-04-11 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
