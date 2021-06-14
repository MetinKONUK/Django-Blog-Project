from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label="username")
    password = forms.CharField(max_length=20, label="password", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="confirm password", widget=forms.PasswordInput)
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm  = self.cleaned_data.get("confirm")
        if password and confirm and confirm != password:
            raise forms.ValidationError("Dont't match!")
        values = {
            "username" : username,
            "password" : password,
        }
        return values

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="username")
    password = forms.CharField(max_length=20, label="password", widget=forms.PasswordInput)
