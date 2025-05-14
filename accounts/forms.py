from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile, CustomUser, Problem


class SignupForm(ModelForm):
    """
    Formulaire de creation de comptes pour  les utilisateurs.
    """
    class Meta:
        model = CustomUser
        fields = ['email', 'password','telephone']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        }

class LoginForm(forms.Form):
    """
    Formulaire de connexion pour les utilisateurs.
    """
    email = forms.EmailField(label='Email', max_length=255,
                                 widget=forms.EmailInput(attrs={
                                     'placeholder': 'Email',
                                     'class': 'form-control'
                                 }))
    password = forms.CharField(label='Mot de passe',
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': 'Mot de passe',
                                       'class': 'form-control'
                                 }))


class SignalerForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'created_by', 'votes_count', 'image_problem']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre du problème'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description détaillée du problème'}),
            'created_by': forms.HiddenInput(),
            'votes_count': forms.NumberInput(attrs={'readonly': True}),
            'image_problem': forms.FileInput(attrs={'accept': 'image/*'})
        }
