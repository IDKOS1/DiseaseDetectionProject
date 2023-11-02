from django.urls import path
from . import views

urlpatterns = [
    path('uploadImage/', views.imagesUpload),
]
