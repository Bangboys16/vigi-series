# Generated by Django 5.0.6 on 2024-07-24 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigi2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='category',
            field=models.CharField(choices=[('korean', 'Korean'), ('indian', 'Indian'), ('hollywood', 'Hollywood'), ('nollywood', 'Nollywood')], default=True, max_length=20),
        ),
    ]
