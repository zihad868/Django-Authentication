from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import LoginForm, UserRegistrationForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . mixins import LogoutRequiredMixins

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

@method_decorator(never_cache, name="dispatch")
class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "account/home.html"
    login_url = 'login'

@method_decorator(never_cache, name="dispatch")
class Login(LogoutRequiredMixins, generic.View):
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

@method_decorator(never_cache, name='dispatch')
class Registration(LogoutRequiredMixins, generic.CreateView):
    template_name = 'account/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, "Registration Success")
        return super().form_valid(form)
    
@method_decorator(never_cache, name='dispatch')
class ChangePassword(LoginRequiredMixin, generic.FormView):
    template_name = "account/changePassword.html"
    form_class = ChangePasswordForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('login')
    
    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context['user'] = self.request.user
        return context
    
    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get('new_password1'))
        user.save()
        messages.success(self.request, "Password Change Successfully")
        return super().form_valid(form)
        