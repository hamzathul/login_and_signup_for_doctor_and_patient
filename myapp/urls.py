from django.urls import path
from myapp import views

urlpatterns = [
    # path('', views.index, name='home'),
    path('login/', views.login),
    path('login_post/', views.login_post),

    path('signup/', views.signup),
    path('signup_post/', views.signup_post),

    path('view_patient/', views.view_patient),
    path('view_doctor/', views.view_doctor),
]