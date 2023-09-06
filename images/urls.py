from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create-image/', views.image_create, name='image_create'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='image_detail'),
    path('like/', views.image_like, name='liked'),
    path('', views.image_list, name='list'),
]  