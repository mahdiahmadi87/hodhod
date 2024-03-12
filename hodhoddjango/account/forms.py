from django.contrib.auth import get_user_model
from django import forms

class SignupForm(forms.Form):
    color = forms.CharField(max_length=30, label='color')

    def signup(self, request, user):
        user.color = self.cleaned_data['color']
        user.save()
