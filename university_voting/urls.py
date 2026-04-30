
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from Voting.models import Position
from Voting.views import signup_view


def home_view(request):
    if request.user.is_authenticated:
        return redirect('vote')
    return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_view, name='home'), 
    path("", include('Voting.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', signup_view, name='signup'), 
]
