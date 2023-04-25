from django.shortcuts import render
import requests
from configparser import ConfigParser
from pathlib import Path

# Create your views here.
def home(request):
    return render(request, 'index.html')

def search(request):
    print("in this func")
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST' and request.POST['zipcode'] and request.POST['units']:
        CONFIG = ConfigParser()
        CONFIG.read(Path(__file__).resolve().parent.parent / "config.ini")
        api_key = CONFIG.get("API", "key")
        print("key:", api_key)
        zip_code = request.POST['zipcode']
        geo_url = 'http://api.openweathermap.org/geo/1.0/zip?zip={}&appid={}'.format(zip_code, api_key)
        response_loc = requests.get(geo_url).json()
        context = {}
        if 'message' in response_loc:
            return render(request, 'index.html', {'message': response_loc['message']})
        else:
            lat = response_loc['lat']
            lon = response_loc['lon']
            context['name'] = response_loc['name']
            context['country'] = response_loc['country']
            call_url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units={}&exclude=minutely,alerts,current&appid={}'.format(lat, lon, request.POST['units'], api_key)
            response_call = requests.get(call_url).json()
            if 'message' in response_call:
                return render(request, 'index.html', {'message': response_call['message']})
            else:
                context['daily'] = response_call['daily'][:7]
                context['hourly'] = response_call['hourly'][:8]
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', {'message': 'You must enter zip code.'})
