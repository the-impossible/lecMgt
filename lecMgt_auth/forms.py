from django import forms
from lecMgt_auth.models import *

class AccountCreationForm(forms.ModelForm):

    USER_TYPES = (
        ("1", "Central Admin"),
        ("5", "System Admin"),
        ("2", "Dean Office"),
        ("4", "Departmental Admin"),
        ("3", "HOD Office"),
        ("6", "Lecturer"),
    )

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'email',
        }
    ))

    name = forms.CharField(help_text='Enter full name', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="(Select Department)", required=True, help_text="Select department",  widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != None:
            if User.objects.filter(email=email.lower().strip()).exists():
                raise forms.ValidationError('Email Already taken!')

        return email


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('12345678'))

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'user_type', 'department')
