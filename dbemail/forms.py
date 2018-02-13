# encoding: utf-8

from django import forms
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.validators import validate_email

from mezzanine.core.forms import TinyMceWidget
from profiles.models import User


class SendEmailForm(forms.Form):
    all_users = forms.BooleanField(required=False,label=u'Send to all users')
    recipients = forms.MultipleChoiceField()
    subject = forms.CharField(required=True, widget=forms.TextInput())
    message = forms.CharField(required=True, widget=forms.Textarea())
    
    def __init__(self, *args, **kwargs):
        choices = self.get_recipient_choices()
        super(SendEmailForm, self).__init__(*args, **kwargs)
        self.fields["recipients"] = forms.MultipleChoiceField(required=False,choices=choices)
        
    def get_recipient_choices(self):
        choices = []
        for user in User.objects.all():
            name = u"%s <%s>" % (user.get_full_name(), user.email)
            choices.append((user.email, name))
        return choices
    
    def all_mail_addresses(self):
        mail_addresses = []
        for user in User.objects.all():
            try:
                email = validate_email(user.email)
            except:
                pass
            else:
                mail_addresses.append(user.email)
        return mail_addresses
    
    def clean(self):
        cleaned_data = self.cleaned_data
        all_users = cleaned_data.get('all_users')
        recipient_list = cleaned_data.get('recipients')
        if not all_users and not recipient_list:
            raise forms.ValidationError(u'Please select some user')
        return cleaned_data
    
    def save(self):
        all_users = self.cleaned_data.get('all_users')
        if all_users:
            recipient_list = self.all_mail_addresses()
        else:
            recipient_list = self.cleaned_data.get('recipients')
        subject = self.cleaned_data.get('subject')
        body = self.cleaned_data.get('message')
        all_users = self.cleaned_data.get('all_users')
        
        message = EmailMessage(subject=subject, 
                               body=body, bcc=recipient_list,)
        return message.send()