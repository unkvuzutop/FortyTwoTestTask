from apps.hello.models import RequestHistory


def get_unread_requests_count(request_ids):
    latest_requests_count = RequestHistory.objects\
        .filter(id__in=request_ids)\
        .filter(is_viewed=False)\
        .count()
    return latest_requests_count
