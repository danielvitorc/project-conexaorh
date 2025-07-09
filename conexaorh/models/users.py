from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('gestor', 'Gestor'),
        ('diretor', 'Diretor'),
        ('presidente', 'Presidente'),
        ('rh', 'RH'),
        ('complice','Complice')
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
User = get_user_model()