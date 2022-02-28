from email import message
from unicodedata import name
import requests 
from django.shortcuts import redirect, render, redirect
from .models import City
from .forms import CityForm
import math
def home(request):
    api_id = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2d6ed05dfaddedb887db0b6fbf06b332'
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(api_id.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'You City is Belongs to Mars ig. City Does not exist in the world'
                    print(err_msg)
            else:
                err_msg = 'City Already Exists in the DataBase'
        if err_msg:
            message = err_msg
            message_class='is-danger'
        else:
            message = 'City Added Successfully!'
            message_class = 'is-success'
    cities = City.objects.all()
    form = CityForm()
    weather_data = []

    for city in cities:

        r = requests.get(api_id.format(city)).json()

        city_weather = {
            'city':city.name,
            'temperature':math.ceil(r['main']['temp']),
            'humidity':r['main']['humidity'],
            'wind':math.ceil(r['wind']['speed']),
            'description':r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        } 
        weather_data.append(city_weather)

    context = {
        'weather_data':weather_data,
        'form':form,
        'message':message,
        'message_class':message_class
}
    return render(request,'Weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect(request,'home')