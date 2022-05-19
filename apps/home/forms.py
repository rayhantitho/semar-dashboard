from django import forms

from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput

class DateForm(forms.Form):
    date_time_field = forms.DateTimeField(widget=DateTimePickerInput)