# Generated by Django 5.0.6 on 2024-07-29 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigi2', '0003_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='vigi2.genre'),
        ),
    ]
