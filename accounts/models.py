from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# 1. Le manager personnalisé 
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# 2. Le modèle personnalisé
class CustomUser(AbstractUser):
    username = None  # On désactive le champ username
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Aucun champ obligatoire en plus de l'email

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)


class Problem(models.Model):
    """
    Modèle représentant un problème soumis par les citoyens.
    """
    title = models.CharField(_('Titre'), max_length=255)
    image_problem=models.ImageField(upload_to='problem/',blank=True,null=True)
    description = models.TextField(_('Description'))
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name=_('Créé par'))
    created_at = models.DateTimeField(_('Créé à'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Mis à jour à'), auto_now=True)
    votes_count = models.IntegerField(_('Nombre de votes'), default=0)

    class Meta:
        verbose_name = _('Problème')
        verbose_name_plural = _('Problèmes')
        ordering = ['-votes_count', '-created_at']  # Les problèmes les plus votés en premier

    def __str__(self):
        return self.title


class Vote(models.Model):
    """
    Modèle représentant un vote pour un problème.
    """
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='votes', verbose_name=_('Problème'))
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name=_('Utilisateur'))
    created_at = models.DateTimeField(_('Créé à'), auto_now_add=True)

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        unique_together = ('problem', 'user')  # Un utilisateur peut voter une seule fois pour un problème

    def __str__(self):
        return f"{self.user} -> {self.problem}"
