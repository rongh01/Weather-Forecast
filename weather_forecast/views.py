from django.shortcuts import render
import requests
from configparser import ConfigParser
from pathlib import Path
import datetime

def home(request):
    return render(request, 'base.html')

def search(request):
    if request.method == 'GET':
        return render(request, 'base.html')
    if request.method == 'POST' and request.POST['zipcode'] and request.POST['units']:
        CONFIG = ConfigParser()
        CONFIG.read(Path(__file__).resolve().parent.parent / "config.ini")
        api_key = CONFIG.get("API", "key")
        zip_code = request.POST['zipcode']
        units = request.POST['units']
        geo_url = 'http://api.openweathermap.org/geo/1.0/zip?zip={}&appid={}'.format(zip_code, api_key)
        response_loc = requests.get(geo_url)
        if response_loc.status_code != 200:
            return render(request, 'base.html', {'message': 'HTTP response status code: ' + str(response_loc.status_code)})
        response_loc_json = response_loc.json()
        context = {}
        context['sign'] = temp_sign(units)
        if 'message' in response_loc_json:
            return render(request, 'base.html', {'message': response_loc_json['message']})
        lat = response_loc_json['lat']
        lon = response_loc_json['lon']
        context['name'] = response_loc_json['name']
        context['country'] = response_loc_json['country']
        call_url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units={}&exclude=minutely,alerts,current&appid={}'.format(lat, lon, units, api_key)
        response_call = requests.get(call_url)
        if response_call.status_code != 200:
            return render(request, 'base.html', {'message': 'HTTP response status code: ' + str(response_loc.status_code)})
        response_call_json = response_call.json()
        days = []
        hours = []
        if 'message' in response_call_json:
            return render(request, 'base.html', {'message': response_call_json['message']})
        for day in response_call_json['daily'][:7]:
            days.append({
                'dt': datetime.datetime.fromtimestamp(day['dt']).strftime('%A'),
                'temp_min': day['temp']['min'],
                'temp_max': day['temp']['max'],
                'description': day['weather'][0]['description'],
                'icon': day['weather'][0]['icon']
            })
        for hour in response_call_json['hourly'][:8]:
            hours.append({
                'dt': datetime.datetime.fromtimestamp(hour['dt']).strftime('%I %p'),
                'temp': hour['temp'],
                'description': hour['weather'][0]['description'],
                'icon': hour['weather'][0]['icon']
            })
        context['days'] = days
        context['hours'] = hours
        return render(request, 'index.html', context)
    return render(request, 'base.html', {'message': 'You must enter zip code.'})


def temp_sign(choice):
    if choice == 'imperial':
        return '°F'
    return '°C'
