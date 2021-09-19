from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import WorldBorder
import requests
import datetime
import dateutil.parser


class IndexView(TemplateView):
    template_name = "world/indexpage.html"


class HomePageView(TemplateView):
    template_name = "world/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        all_countries = WorldBorder.objects.all()
        context.update({"all_countries": all_countries})
        return context


class LocationDetailView(View):
    template_name = "world/detail.html"

    def get(self, request, *args, **kwargs):
        context = {}
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        context.update({"latitude":float(latitude), "longitude":float(longitude)})

        grid_point_response = requests.get("https://api.weather.gov/points/{},{}".format(latitude, longitude))
        if grid_point_response.status_code == 200:
            grid_endpoint = grid_point_response.json().get("properties", {}).get("forecastGridData")
            if grid_endpoint:
                forecast_response = requests.get(grid_endpoint)

                temperature_data = forecast_response.json().get("properties", {}).get("temperature", {}).get("values", {})
                humidity_data = forecast_response.json().get("properties", {}).get("relativeHumidity", {}).get("values", {})
                current_date_time = datetime.datetime.now().replace(minute=0,second=0, microsecond=0)
                for data in temperature_data:
                    iso_time = data.get("validTime")
                    iso_time = iso_time.split("/")[0]
                    date_time = dateutil.parser.parse(iso_time).replace(minute=0,second=0, microsecond=0, tzinfo=None)

                    if current_date_time == date_time:
                        context.update({"temperature": data.get("value")})
                        break

                for data in humidity_data:
                    iso_time = data.get("validTime")
                    iso_time = iso_time.split("/")[0]
                    date_time = dateutil.parser.parse(iso_time).replace(minute=0,second=0, microsecond=0, tzinfo=None)

                    if current_date_time == date_time:
                        context.update({"humidity": data.get("value")})
                        break


                return render(request,"world/detail.html",context)

            else:
                return HttpResponse("Grid API Endpoint not returned", status=200)

        else:
            return HttpResponse("Weather API is giving 404 for this latitude and longitude", status=200)




