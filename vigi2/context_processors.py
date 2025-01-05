from .models import Episode
from datetime import date


def episode_context(request):
    today = date.today()
    episode_today_count = Episode.objects.filter(posted_at__gte=today).count() 
    return {'episode_today_count': episode_today_count}
 