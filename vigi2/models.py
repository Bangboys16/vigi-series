# vigiseries/models.py
from django.db import models
from decimal import Decimal

class Series(models.Model):
    CATEGORY_CHOICES = [
        ('korean', 'Korean'),
        ('indian', 'Indian'),
        ('hollywood', 'Hollywood'),
        ('nollywood', 'Nollywood'),
        ('other', 'Other')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    genres = models.ManyToManyField('Genre', related_name='movies')
    poster = models.ImageField(upload_to='series_posters/')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=True)
    
    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Episode(models.Model):
    series = models.ForeignKey(Series, related_name='episodes', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    episode_number = models.PositiveIntegerField()
    season_number = models.PositiveIntegerField()
    release_date = models.DateField()
    video_file = models.FileField(upload_to='series_episodes/')
    subtitle_file = models.FileField(upload_to='episode_subtitles/', blank=True, null=True)
    # Add file_size field to store the size of the movie file in MB
    file_size = models.IntegerField(default=0)

    # New fields for ratings
    rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.series.title} - S{self.season_number}E{self.episode_number}: {self.title}"

    def update_rating(self, new_rating):
        # Ensure new_rating is a Decimal
        if isinstance(new_rating, float):
            new_rating = Decimal(new_rating)

        # Convert current rating to Decimal for consistency
        current_rating = Decimal(self.rating)  # Convert float to Decimal
        total_ratings = current_rating * Decimal(self.rating_count)  # Ensure multiplication is consistent
        total_ratings += new_rating  # Now it's safe to add Decimal
        self.rating_count += 1
        self.rating = total_ratings / Decimal(self.rating_count)  # Ensure division is also consistent
        self.save()



class Comment(models.Model):
    series = models.ForeignKey('Series', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)  # Field for the name
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.comment

class Subtitle(models.Model):
    series = models.ForeignKey('Series', related_name='subtitles', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    file = models.FileField(upload_to='subtitles/')

    def __str__(self):
        return f"{self.language} subtitle for {self.series.title}"