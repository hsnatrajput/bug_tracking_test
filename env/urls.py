from django.urls import path
from django.contrib.auth import views as auth_views
from.import views


urlpatterns = [
    path('signup/' , views.signup , name='signup'),
    path('login/' , views.login , name='login' ),
    path('logout/', auth_views.Logout_view.as_view() , name='logout'),
    path('dashboard/',views.dashboard , name='dashboard')
]

