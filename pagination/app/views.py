import csv
from urllib.parse import urlencode

from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator


def read_csv():
    info = []
    csv_file_path = settings.BUS_STATION_CSV
    with open(csv_file_path, encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            info.append(row)
    return info


def get_url_with_param(page):
    param = {'page': page}
    url = reverse('bus_stations')
    encode_param = urlencode(param)
    bus_url = '?'.join((url, encode_param))
    return bus_url


def index(request):
    page = int(request.GET.get('page', 1))
    bus_url = get_url_with_param(page)
    return redirect(bus_url)


def bus_stations(request):
    info = read_csv()
    paginator = Paginator(info, 10)
    current_page = int(request.GET.get('page', 1))
    current_info = paginator.get_page(current_page)
    prev_page_url, next_page_url = None, None
    data = current_info.object_list
    if current_info.has_previous():
        prev_page = current_info.previous_page_number()
        prev_page_url = get_url_with_param(prev_page)
    if current_info.has_next():
        next_page = current_info.next_page_number()
        next_page_url = get_url_with_param(next_page)
    return render_to_response('index.html', context={
        'bus_stations': data,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

