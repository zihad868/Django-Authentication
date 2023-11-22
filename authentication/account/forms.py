from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()



class LoginForm(forms.Form):
    def __in__(self, *args, **kwargs):
        super().__init__(**args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    
    def __in__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        
        if model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("User name exist")
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        
        if model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("User Email exist")
        
        return email
        
    
    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.data.get('password2')
        
        if password and password2:
            if password != password2:
                raise forms.ValidationError("Password mismatch")
        return password
    
    def save(self, commit=True, *args, **kwrgs):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))
        
        if commit:
            user.save()
            
        return user