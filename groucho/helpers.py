
def get_source_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    # todo: try looking for other headers when missing
    if not ip:
        ip = request.META.get('REMOTE_ADDR')

    # if there's a list of them then split and take the last
    return ip.split(',')[-1]
