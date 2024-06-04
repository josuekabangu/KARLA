from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.core.exceptions import ValidationError

# Define your custom password validator
def validate_password_special_characters(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError('Le mot de passe doit contenir au moins un chiffre.')
    if not any(char.isalpha() for char in value):
        raise ValidationError('Le mot de passe doit contenir au moins une lettre.')
    if not any(char in '!@#$%^&*()_+' for char in value):
        raise ValidationError('Le mot de passe doit contenir au moins un caractère spécial.')

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, help_text='Optional.') 
    last_name = models.CharField(max_length=50, blank=True, help_text='Optional.') 
    email = models.EmailField(blank=False, help_text='Required.', validators=[EmailValidator()])
    is_client = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)

    # Champ de mot de passe avec validateur personnalisé
    password = models.CharField(max_length=100, validators=[validate_password_special_characters])

    def save(self, *args, **kwargs):
        # Vous pouvez également effectuer des opérations supplémentaires ici avant de sauvegarder l'utilisateur
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    class Meta:
        db_table = 'accounts_employee'

    def __str__(self):
        return self.user.username
