# vigiseries/models.py
from django.db import models
from decimal import Decimal
from django.utils.text import slugify

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
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    trailer_url = models.URLField(max_length=300, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True)  # Add slug field

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if it's not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

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
    file_size = models.IntegerField(default=0)
    posted_at = models.DateTimeField(auto_now_add=True)
    # Fields for ratings
    rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    # New slug field for the episode
    slug = models.SlugField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if it's not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.series.title} - S{self.season_number}E{self.episode_number}: {self.title}"

    def update_rating(self, new_rating):
        if isinstance(new_rating, float):
            new_rating = Decimal(new_rating)
        current_rating = Decimal(self.rating)
        total_ratings = current_rating * Decimal(self.rating_count)
        total_ratings += new_rating
        self.rating_count += 1
        self.rating = total_ratings / Decimal(self.rating_count)
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