from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.conf.urls import url
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _

from .forms import SendEmailForm

@staff_member_required
def send_mail(request, extra_context=None):
        if request.POST:
            form = SendEmailForm(request.POST)
            if form.is_valid():
                form.save()
                post_url = reverse('admin:index',)
                messages.success(request, u'Your message has been sent.',)
                return HttpResponseRedirect(post_url)
        else:
            form = SendEmailForm()
        
        title = _("Send Mail")

        context = {
            "title": title,
            "form": form,
        }
        context.update(extra_context or {})

        return TemplateResponse(request, ["admin/send_mail.html",], context, )