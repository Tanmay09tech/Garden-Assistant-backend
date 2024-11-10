from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'), 
    path('api/plants/<str:plant_name>/', views.get_plant_data, name='get_plant_data'),
]
