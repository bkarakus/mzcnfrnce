# coding: utf-8
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

from mezzanine.accounts.forms import ProfileForm as MezzanineProfileForm

from profiles.models import alphanumeric_regex, alphanumeric_message

class ProfileForm(MezzanineProfileForm):
    helper = FormHelper()
    helper.form_show_labels = True
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('first_name', css_class='col-md-6'),
            Div('last_name', css_class='col-md-6'),  
            css_class='row'
        ),
        Div(
            Div('username', css_class='col-md-6'),
            Div('email', css_class='col-md-6'),  
            css_class='row'
        ),
        Div(
            Div('password1', css_class='col-md-6'),
            Div('password2', css_class='col-md-6'),  
            css_class='row'
        ),
        Div(
            Div('title', css_class='col-md-6'),
            Div('name', css_class='col-md-6'),  
            css_class='row'
        ),
        Div(
            Div('university', css_class='col-md-6'),
            Div('department', css_class='col-md-6'),
            css_class='row'
        ),
        Div(
            Div('country', css_class='col-md-6'),
            Div('phone', css_class='col-md-6'),
            css_class='row'
        ),
    )
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(alphanumeric_regex, name):
            raise forms.ValidationError(alphanumeric_message)
        return name
    
    def clean_university(self):
        university = self.cleaned_data['university']
        if not re.match(alphanumeric_regex, university):
            raise forms.ValidationError(alphanumeric_message)
        return university
    
    def clean_department(self):
        department = self.cleaned_data['department']
        if not re.match(alphanumeric_regex, department):
            raise forms.ValidationError(alphanumeric_message)
        return department
    