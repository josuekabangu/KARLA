# accounts/views.py
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect

User = get_user_model()

# Create your views here.
def profile_user(request):
  return render(request, 'accounts/profile.html') 

def signup(request):
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")
        
    # Valider le mot de passe
    try:
      validate_password(password)
    except ValidationError as e:
      # Si la validation échoue, récupérez les messages d'erreur et renvoyez-les à la page signup
      error_message = '\n'.join(e.messages)
      return render(request, 'accounts/signup.html', {'error_message': error_message})
        
    # Vérifiez si un utilisateur avec le même nom d'utilisateur existe
    if User.objects.filter(username=username).exists():
      # L'utilisateur existe déjà, redirigez-le vers la page de connexion
      return redirect('login')  # Assurez-vous que 'login' correspond à l'URL de votre page de connexion
    else:
      # L'utilisateur n'existe pas, créez-le
      user = User.objects.create_user(
      username=username,
      password=password
      )
      
      login(request, user)
      return redirect('profile')  # Redirigez l'utilisateur vers la page d'accueil ou une autre page appropriée

  return render(request, 'accounts/signup.html')

def login_user(request):
  error_message = None
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)

    if user:
      login(request, user)
      return redirect('profile')
    else:
      error_message = "Identification ou mot de passe incorrecte"  # Message d'erreur en cas d'authentification échouée

  return render(request, 'accounts/login.html', {'error_message': error_message})


def logout_user(request):
  logout(request)
  return redirect('login')


