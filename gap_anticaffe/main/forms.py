from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class AddClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Clients
        fields = ['fio', 'slug', 'birth_date', 'address', 'phone', 'e_mail', 'photo']
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'e_mail': forms.TextInput(attrs={'class': 'form-control'}),
        }
        # TODO: Доделать если будет необходимо собственные валидаторы для полей


class AddBranchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = "Пользователь не выбран"

    class Meta:
        model = Branch
        fields = ['address', 'slug', 'phone', 'user']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
        }


class AddGoodsAndServicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].empty_label = "Заведение не выбрано"

    class Meta:
        model = GoodsAndServices
        fields = ['name', 'slug', 'group', 'description', 'remaining_quantity', 'branch']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'remaining_quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }


class AddPriceListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['good_or_service'].empty_label = "Товар/услуга не выбраны"

    class Meta:
        model = PriceList
        fields = ['good_or_service', 'slug', 'price']
        widgets = {
            'good_or_service': forms.Select(attrs={'class': 'form-select'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'})
        }


class AddSuppliersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Suppliers
        fields = ['fio', 'slug', 'inn', 'phone', 'e_mail']
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'e_mail': forms.TextInput(attrs={'class': 'form-control'})
        }


class AddContractsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['good_or_service'].empty_label = "Товар/Услуга не выбраны"
        self.fields['supplier'].empty_label = "Поставщик не выбран"

    class Meta:
        model = Contracts
        fields = ['good_or_service', 'slug', 'supplier', 'quantity', 'price', 'delivery_schedule']
        widgets = {
            'good_or_service': forms.Select(attrs={'class': 'form-select'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_schedule': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddEventsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].empty_label = "Заведение не выбрано"

    class Meta:
        model = Events
        fields = ['name', 'slug', 'description', 'date_time_of_event', 'max_num_of_participants', 'current_num_of_participants', 'price', 'branch']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date_time_of_event': forms.TextInput(attrs={'class': 'form-control'}),
            'max_num_of_participants': forms.TextInput(attrs={'class': 'form-control'}),
            'current_num_of_participants': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }


class AddReservationsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].empty_label = "Заведение не выбрано"
        self.fields['event'].empty_label = "Мероприятие не выбрано"

    class Meta:
        model = Reservations
        fields = ['date_time_of_reservation', 'slug', 'client_name', 'object_of_reservation', 'event', 'table_num', 'branch', 'num_of_persons']
        widgets = {
            'date_time_of_reservation': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'object_of_reservation': forms.TextInput(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-select'}),
            'table_num': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'num_of_persons': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddVisitsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].empty_label = "Заведение не выбрано"
        self.fields['client'].empty_label = "Клиент не выбран"
        self.fields['reservation'].empty_label = "Бронирование не выбрано"

    class Meta:
        model = Visits
        fields = ['date_of_visit', 'slug', 'client', 'goods_and_services', 'is_reserved', 'reservation', 'time_start', 'time_end', 'payment_price', 'branch']
        widgets = {
            'date_of_visit': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'goods_and_services': forms.Textarea(attrs={'class': 'form-control'}),
            'reservation': forms.Select(attrs={'class': 'form-select'}),
            'time_start': forms.TextInput(attrs={'class': 'form-control'}),
            'time_end': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_price': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }


class AddStaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].empty_label = "Заведение не выбрано"

    class Meta:
        model = Staff
        fields = ['last_name', 'first_name', 'patronymic', 'slug', 'birth_date', 'address', 'phone', 'e_mail', 'num_of_employment_contract', 'duration_of_contract', 'salary', 'branch']
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'e_mail': forms.TextInput(attrs={'class': 'form-control'}),
            'num_of_employment_contract': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_of_contract': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))


class DelForm(forms.Form):
    delete = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'hid', 'placeholder': '111'}), initial='111')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))

    class Meta:
        model = User
        fields = {'username', 'password1', 'password2'}


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
