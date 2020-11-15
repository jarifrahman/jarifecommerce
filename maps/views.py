from django.shortcuts import render, HttpResponse
import requests
# Create your views here.
def map(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
    response = requests.get('http://freegeoip.net/json/%s' % ip_address)
    geodata = response.json()
    return render(request, 'map.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'latitude': geodata['latitude'],
        'longitude': geodata['longitude'],
        'api_key': 'AIzaSyC74lMb-qCFqWVzjVJ7V_Y_f-3DZXMXzH8'  # Don't do this! This is just an example. Secure your keys properly.
    })


def getipaddress(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return render(request, 'map.html', {'ip':ip})

'''
def getapiaddress2(request):
    is_cached = ('geodata' in request.session)

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        response = requests.get('http://freegeoip.net/json/%s' % ip_address)
        request.session['geodata'] = response.json()

    geodata = request.session['geodata']

    return render(request, 'map.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'latitude': geodata['latitude'],
        'longitude': geodata['longitude'],
        'api_key': 'AIzaSyC74lMb-qCFqWVzjVJ7V_Y_f-3DZXMXzH8',  # Don't do this! This is just an example. Secure your keys properly.
        'is_cached': is_cached
    })

    '''