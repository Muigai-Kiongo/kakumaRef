from django.utils import timezone
from datetime import timedelta

def filter_by_timeframe(queryset, timeframe, date_field='date'):
    now = timezone.now()
    if timeframe == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif timeframe == 'monthly':
        start_date = now - timedelta(days=30)
    elif timeframe == 'yearly':
        start_date = now - timedelta(days=365)
    else:
        return queryset.all()  # 'all' or invalid timeframe
    
    return queryset.filter(**{f'{date_field}__gte': start_date})
