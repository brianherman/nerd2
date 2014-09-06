import datetime
from collections import Counter

def main(request):
    statuses = {'open': 2, 'claimed': 1, 'closed': 0}
    server = request.args.get('server', None)
    format = request.args.get('format', None)
    _filter = request.args.get('filter', None)
    sort = request.args.get('sort', 'desc')
    try:
        limit = int(request.args.get('limit', 100))
    except ValueError:
        limit = 100
    try:
        refresh = int(request.args.get('refresh', False))
    except ValueError: 
        refresh = False
    else:
        if refresh != 0 and refresh < 90:
            refresh = 90

    if _filter != None and _filter.lower() in ['closed', 'claimed', 'open']:
        filter_query = 'WHERE status = %s' % statuses[_filter]
    else:
        filter_query = ''
    if sort.lower() not in ['asc', 'desc']:
        sort = 'desc'

    return server, limit, format, refresh, filter_query, sort

def graph(modreqs):
    c = Counter()
    for req in modreqs:
        reqDate = datetime.date.fromtimestamp(req['request_time']/1000).strftime('%Y/%m/%d')
        c[reqDate] += 1
    return c

def formatRequests(requests, server):
    ''' Removes location for survival modreqs '''
    statuses = {2: 'Open', 1:'Claimed', 0: 'Closed'}
    for req in requests:
        req['status'] = statuses[req['status']]
        if server == 'survival':
            del(req['request_location'])

    return requests