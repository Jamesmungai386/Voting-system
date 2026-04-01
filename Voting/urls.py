from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('vote/', views.vote_view, name='vote'),
    path('results/', views.results_view, name='results'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/signup/', views.signup_view, name='signup'),
]
