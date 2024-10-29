# Generated by Django 5.0.6 on 2024-08-04 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigi2', '0004_series_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='category',
            field=models.CharField(choices=[('korean', 'Korean'), ('indian', 'Indian'), ('hollywood', 'Hollywood'), ('nollywood', 'Nollywood'), ('other', 'Other')], default=True, max_length=20),
        ),
    ]
