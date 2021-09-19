from django.urls import path
from django.urls import path
from .views import HomePageView, LocationDetailView

urlpatterns = [
    path('homepage/', HomePageView.as_view(), name="homepage"),
    path('details/', LocationDetailView.as_view(), name="location-detail"),
]
