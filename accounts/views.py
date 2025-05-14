from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView

from accounts.forms import LoginForm, SignupForm, SignalerForm
from accounts.models import Problem

User = get_user_model()





def home(request):
    return render(request, 'accounts/index.html')

def signup(request):
    """
    Vue pour gérer la création d'un compte utilisateur via un formulaire.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            telephone = form.cleaned_data['telephone']

            # Vérifier l'existence d'un utilisateur avec cet email ou ce téléphone
            if User.objects.filter(email=email).exists():
                messages.error(request, _("Un utilisateur avec cet email existe déjà."))
                return render(request, 'accounts/create_account.html', {'form': form})
            if User.objects.filter(telephone=telephone).exists():
                messages.error(request, _("Un utilisateur avec ce numéro de téléphone existe déjà."))
                return render(request, 'accounts/create_account.html', {'form': form})

            # Créer l'utilisateur
            User.objects.create_user(email=email, password=password, telephone=telephone)
            messages.success(request, _("Votre compte a été créé avec succès !"))
            return redirect('home')  # Changez l'URL 'login' par l'URL vers votre page de connexion
    else:
        form = SignupForm()

    return render(request, 'accounts/create_account.html', {'form': form})


def login_view(request):
    """
    Vue pour gérer la connexion d'un utilisateur.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authentifier l'utilisateur
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _("Vous êtes connecté avec succès !"))
                return redirect('home')  # Changez l'URL 'home' par l'URL vers votre page d'accueil
            else:
                messages.error(request, _("Identifiants invalides. Veuillez réessayer."))

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})






class CreateSignal(CreateView):
    model = Problem
    template_name = 'accounts/signaler.html'
    form_class = SignalerForm
    success_url = '/home'  # Redirigez vers la page d'accueil après la soumission réussie du formulaire


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.votes_count = 0
        return super().form_valid(form)



class UpdateSignal(UpdateView):
    model = Problem
    template_name = 'accounts/signaler.html'
    form_class = SignalerForm
    success_url = '/home'

