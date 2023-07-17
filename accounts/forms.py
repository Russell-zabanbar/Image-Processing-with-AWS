from django import forms
from accounts.models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


def check_number(value):
    if value[:2] != "09" or len(value) < 11:
        raise ValidationError('یک شماره تماس معتبر وارد کنید', code='check_number')
    try:
        int(value)
    except:
        raise ValidationError('یک شماره تماس معتبر وارد کنید', code='check_number')


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password', 'is_admin', 'is_active', 'is_baker')


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\"../password/\">this form</a>.")


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': ' شماره موبایل خود را وارد نمایید ', 'maxlength': 11}),
        validators=[check_number])


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()
