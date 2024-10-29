# vigiseries/admin.py
from django.contrib import admin
from .models import Genre, Series, Episode, Comment, Subtitle

class SubtitleInline(admin.TabularInline):
    model = Subtitle

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1

class SeriesAdmin(admin.ModelAdmin):
    inlines = [EpisodeInline]

admin.site.register(Series, SeriesAdmin)
admin.site.register(Genre)
admin.site.register(Episode)
admin.site.register(Comment)   
