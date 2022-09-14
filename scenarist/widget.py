from django import forms
from datetimepicker.widgets import DateTimePicker


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'
    widget = DateTimePicker()