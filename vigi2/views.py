# vigiseries/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Series, Episode, Comment
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import RatingForm
from random import shuffle
from datetime import date


def series_list(request):
    query = request.GET.get('q', '')  # Set default to an empty string if no query is provided
    
    # Filter series based on the query and order them by release_date (newest first)
    if query:
        series_list = Series.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by('-release_date')
    else:
        series_list = Series.objects.all().order_by('-release_date')  # Order by release date

    # Implement pagination (12 series per page)
    paginator = Paginator(series_list, 12)
    page_number = request.GET.get('page')
    series_page = paginator.get_page(page_number)

    return render(request, 'vigi2/series_list.html', {'series_list': series_page, 'query': query})

def get_related_series(series):
    # Get the genres of the current series
    genres = series.genres.all()

    # Find other series with at least one genre in common, excluding the current series
    related_series = Series.objects.filter(genres__in=genres).exclude(id=series.id).distinct()

    # Shuffle the list of related series and limit to 4
    related_series_list = list(related_series)
    shuffle(related_series_list)  # Shuffle the list
    return related_series_list[:5]

def series_detail(request, slug):
    # Fetch the series using the slug
    series = get_object_or_404(Series, slug=slug)
    
    # Fetch comments for the series
    comments = series.comments.all().order_by('-created_at')

    # Get related series based on shared genres
    related_series = get_related_series(series)
    
    if request.method == 'POST':
        # Retrieve name and comment from form submission
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        
        # Ensure both fields are filled before creating the comment
        if name and comment:
            Comment.objects.create(series=series, name=name, comment=comment)
            return redirect('series_detail', slug=series.slug)  # Redirect with slug
    
    return render(request, 'vigi2/series_detail.html', {
        'series': series,
        'comments': comments,
        'trailer_url': series.trailer_url,
        'related_series': related_series, # Pass related series to template
    })


def episode_detail(request, series_slug, episode_slug):
    # Fetch the series and episode using slugs
    series = get_object_or_404(Series, slug=series_slug)
    episode = get_object_or_404(Episode, slug=episode_slug, series=series)
    form = RatingForm()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            episode.update_rating(rating)
            return redirect('episode_detail', series_slug=series.slug, episode_slug=episode.slug)

    return render(request, 'vigi2/episode_detail.html', {
        'episode': episode,
        'file_size': episode.file_size,
        'form': form,
    })



def category_list(request, category):
    series = Series.objects.filter(category=category)

    paginator = Paginator(series, 9)
    page_number = request.GET.get('page')
    series = paginator.get_page(page_number)

    return render(request, 'vigi2/category_list.html', {'series': series, 'category': category})



