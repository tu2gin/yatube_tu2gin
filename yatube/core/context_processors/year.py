import datetime as dt


def year(request):
    current_dt = dt.datetime.now()
    return {'year': current_dt.year, }
