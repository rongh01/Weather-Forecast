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
        response_loc = requests.get(geo_url).json()
        context = {}
        context['sign'] = temp_sign(units)
        if 'message' in response_loc:
            return render(request, 'base.html', {'message': response_loc['message']})
        else:
            lat = response_loc['lat']
            lon = response_loc['lon']
            context['name'] = response_loc['name']
            context['country'] = response_loc['country']
            call_url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units={}&exclude=minutely,alerts,current&appid={}'.format(lat, lon, units, api_key)
            response_call = requests.get(call_url).json()
            days = []
            hours = []
            if 'message' in response_call:
                return render(request, 'base.html', {'message': response_call['message']})
            else:
                for day in response_call['daily'][:7]:
                    days.append({
                        'dt': datetime.datetime.fromtimestamp(day['dt']).strftime('%A'),
                        'temp_min': day['temp']['min'],
                        'temp_max': day['temp']['max'],
                        'description': day['weather'][0]['description'],
                        'icon': day['weather'][0]['icon']
                    })
                for hour in response_call['hourly'][:8]:
                    hours.append({
                        'dt': datetime.datetime.fromtimestamp(hour['dt']).strftime('%I %p'),
                        'temp': hour['temp'],
                        'description': hour['weather'][0]['description']
                    })
                context['days'] = days
                context['hours'] = hours
        return render(request, 'index.html', context)
    else:
        return render(request, 'base.html', {'message': 'You must enter zip code.'})


def temp_sign(choice):
    if choice == 'imperial':
        return '°F'
    return '°C'
