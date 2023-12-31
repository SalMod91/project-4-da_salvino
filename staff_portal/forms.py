from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomStaffUser
from django.core.exceptions import ValidationError

class StaffUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomStaffUser
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomStaffUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already in use.")
        return username

        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match.")