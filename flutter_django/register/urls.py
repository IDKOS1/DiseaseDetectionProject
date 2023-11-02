from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView),
    path('login/', views.LoginView),
    path('checkToken/', views.checkToken),
    path('uploadImage/', views.imagesUpload),
    path('loadResult/', views.resultView)
]
