def get_unreaded_requests_count(requests):
    latest_requests_count = 0
    for request in requests:
        if not request.is_viewed:
            latest_requests_count += 1
    return latest_requests_count
