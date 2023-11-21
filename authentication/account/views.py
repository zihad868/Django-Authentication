from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "account/home.html"
    login_url = 'login'

class Login(generic.View):
    def get(self, *args,**kwargs):
        form = LoginForm()
        context = {'form': form}
        return render(self.request, 'account/login.html', context)
    
    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)

        if form.is_valid():
            user = authenticate(
                self.request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(self.request, user)
                return redirect('home')

            else:
                messages.warning(self.request, "Wrong credentials")
                return redirect('login')

        return render(self.request, 'account/login.html', {'form': form})

class Logout(generic.View):
    def get(self, *args,**kwargs):
        logout(self.request)
        return redirect('login')