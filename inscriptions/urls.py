from django.urls import path
from . import views

app_name = 'inscriptions'
urlpatterns = [
    path('', views.index, name='index'),
    path('validation/', views.validation, name='validation'),
    path('save/', views.save, name='save'),
    path('reject/', views.reject, name='reject')
]
