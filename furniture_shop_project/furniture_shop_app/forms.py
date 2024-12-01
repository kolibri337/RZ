from django import forms
from .models import Good, Order, Client
import datetime

class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['title', 'description', 'price', 'mass']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'mass': 'Масса',
        }

class OrderForm(forms.ModelForm):
    id_good = forms.ModelChoiceField(queryset=Good.objects.all(), label='Товар', to_field_name='title')
    delivery = forms.ChoiceField(choices=[('Курьер', 'Курьер'), ('Самовывоз', 'Самовывоз')], label='Способ доставки')

    class Meta:
        model = Order
        fields = ['id_good', 'quantity', 'delivery']
        labels = {
            'id_good': 'Товар',
            'quantity': 'Количество',
            'delivery': 'Способ доставки',
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['data'] = forms.DateField(initial=datetime.date.today, widget=forms.HiddenInput())

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['type', 'surname', 'name', 'patronymic', 'phone', 'shirota', 'dolgota']
        labels = {
            'type': 'Тип',
            'surname': 'Фамилия',
            'name': 'Имя',
            'patronymic': 'Отчество',
            'phone': 'Телефон',
            'shirota': 'Широта',
            'dolgota': 'Долгота',
        }

class LogoutForm(forms.Form):
    pass