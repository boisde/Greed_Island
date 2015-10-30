def paginator(queryset, page, count, limit=True):
    if count > 20 or count <= 0:
        count = 20
    if page <= 0:
        page = 1

    amount = queryset.count()

    if not limit:
        content = queryset
    else:
        start = (page - 1) * count
        end = start + count
        content = queryset[start:end]

    return amount, content
