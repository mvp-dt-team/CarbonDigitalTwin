import datetime

from django import forms
from django.core.exceptions import ValidationError


class AddBlockForm(forms.Form):
    blockname = forms.CharField(
        max_length=50,
        required=True,
        label="Название блока",
        widget=forms.TextInput(attrs={"class": "form-control rounded"}),
    )

    sensors = forms.MultipleChoiceField(
        required=True,
        label="Выбор датчиков",
        widget=forms.SelectMultiple(attrs={"class": "form-control", "id": "sensors"}),
    )

    properties = forms.MultipleChoiceField(
        required=True,
        label="Выбор свойств",
        widget=forms.SelectMultiple(
            attrs={"class": "form-control", "id": "properties"}
        ),
    )

    model_file = forms.FileField(
        required=True,
        label="Загрузка файла модели",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    model_name = forms.CharField(
        max_length=100,
        required=True,
        label="Название модели",
        widget=forms.TextInput(attrs={"class": "form-control rounded"}),
    )

    model_description = forms.CharField(
        max_length=500,
        required=False,
        label="Описание модели",
        widget=forms.Textarea(attrs={"class": "form-control rounded"}),
    )

    model_type = forms.CharField(
        max_length=50,
        required=True,
        label="Тип блока",
        widget=forms.TextInput(attrs={"class": "form-control rounded"}),
    )
