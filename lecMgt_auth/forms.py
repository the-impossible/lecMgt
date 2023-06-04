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
            'class': 'form-control',
        }
    ))

    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="(Select Department)", required=True, help_text="Select department",  widget=forms.Select(
        attrs={
            'class': 'form-control',
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
        user.set_password('12345678')

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'user_type', 'department')


USER_TYPES = (
    ("1", "Central Admin"),
    ("5", "System Admin"),
    ("2", "Dean Office"),
    ("4", "Departmental Admin"),
    ("3", "HOD Office"),
    ("6", "Lecturer"),
)


class EditAccountCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user_type = kwargs.pop('types', None)
        super(EditAccountCreationForm, self).__init__(*args, **kwargs)
        if self.user_type.is_central:
            self.initial['user_type'] = USER_TYPES[0]
        elif self.user_type.is_dean:
            self.initial['user_type'] = USER_TYPES[2]
        elif self.user_type.is_hod:
            self.initial['user_type'] = USER_TYPES[4]
        elif self.user_type.is_dept:
            self.initial['user_type'] = USER_TYPES[3]
        elif self.user_type.is_staff:
            self.initial['user_type'] = USER_TYPES[1]
        else:
            self.initial['user_type'] = USER_TYPES[5]

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
            'class': 'form-control',
        }
    ))

    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="(Select Department)", required=True, help_text="Select department",  widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    pics = forms.ImageField(required=False, help_text="account profile picture", widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'user_type', 'department', 'pics')
