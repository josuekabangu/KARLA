from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_user, name='profile'),
    path('signup/', views.signup, name='signup'),  # Assurez-vous que la vue est nommée 'signup'
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]