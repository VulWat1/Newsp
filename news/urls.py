from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.news, name='newsHome'),
    path('<int:pk>', views.NewsDet.as_view(), name='newsD')
]