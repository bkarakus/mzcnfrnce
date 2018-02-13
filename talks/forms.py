from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.layout import Layout, Field, Div

from talks.models import Talk, Author

UserModel = get_user_model()

class AuthorForm(forms.ModelForm):
    name = forms.CharField(label=_('name'), max_length=100, required=False)
    email = forms.EmailField(label=_('email'), required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        profile = cleaned_data.get('profile', None)
        name = cleaned_data.get('name', None)
        email = cleaned_data.get('email', None)
        if not profile and (not name or not email):
            raise forms.ValidationError(_('Provide either user or [name and email]'))
        return cleaned_data
        
    class Meta:
        model = Author
        fields = ('profile', 'name', 'email', 'is_presenter',)


class TalkForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = True
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('talk_type', css_class='col-md-6'),
            Div('talk_subject', css_class='col-md-6'),  
            css_class='row'
        ),
        Div(
            Div('title', css_class='col-md-12'),
            css_class='row'
        ),
        
        Div(
            Div('abstract', css_class='col-md-12'),
            css_class='row'
        ),
                           
        Div(
            Div('aippaper', css_class='col-md-12'),
            css_class='row'
        ),
    )
    class Meta:
        model = Talk
        fields = ('title', 'talk_type', 'talk_subject', 'abstract')
        
class AIPPaperForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('aippaper', )
        
AuthorFormSet = inlineformset_factory(Talk, Author,
                                            form=AuthorForm, extra=3, max_num=7)

class AuthorFormSetHelper(FormHelper):
    template = 'bootstrap/table_inline_formset.html'
    def __init__(self, *args, **kwargs):
        super(AuthorFormSetHelper, self).__init__(*args, **kwargs)
        self.add_input(Submit("submit", "Save"))
