from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'images'

urlpatterns = [
    path('', views.image_list, name='list'),
    # path('create/', login_required(views.ImageCreate.as_view()), name='create'),
    path('create/', views.image_create, name='create'),
    # path('detail/<int:id>/<slug:slug>/', views.ImageDetailView.as_view(), name='detail'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
]
