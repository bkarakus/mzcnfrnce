from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template import Template, Context, loader, TemplateDoesNotExist
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.defaultfilters import striptags

from mezzanine.core.models import SiteRelated, Slugged


@python_2_unicode_compatible
class EmailLog(SiteRelated):

    """Model to store outgoing email information"""

    from_email = models.TextField(_("from email"))
    recipients = models.TextField(_("recipients"))
    subject = models.TextField(_("subject"))
    body = models.TextField(_("message"))
    ok = models.BooleanField(_("ok"), default=False, db_index=True)
    date_sent = models.DateTimeField(_("date sent"), auto_now_add=True,
                                     db_index=True)

    def __str__(self):
        return "{s.recipients}: {s.subject}".format(s=self)

    class Meta:
        verbose_name = _("email log")
        verbose_name_plural = _("email logs")
        ordering = ('-date_sent',)

class EmailTemplate(Slugged):
    base_template = models.CharField(max_length=1024, blank=True, help_text="If present, the name of a django template.<br/> The body field will be present as the 'email_body' context variable")
    subject = models.CharField(max_length=1024)
    from_address = models.CharField(max_length=1024, blank=True, null=True, help_text="Specify as: 'Full Name &lt;email@address>'<br/>Defaults to: 'no-reply@site.domain'")
    body = models.TextField(default='')
    txt_body = models.TextField(u'Email Body', default='', help_text="If present, use as the plain-text body")

    def render(self, context):
        if self.base_template:
            try:
                t = loader.get_template(self.base_template)
                context.update({'email_body': self._render_from_string(self.body, context)})
                return t.render(Context(context))
            except TemplateDoesNotExist as e:
                pass
        return self._render_from_string(self.body, context)

    def render_txt(self, context):
        if self.txt_body:
            return self._render_from_string(self.txt_body, context)

    def visible_from_address(self):
        if self.from_address:
            return self.from_address
        default_settings_email = getattr(settings, 'EMAILTEMPLATES_DEFAULT_FROM_EMAIL', None)
        if default_settings_email:
            return default_settings_email
        site = Site.objects.get_current()
        if site.name:
            return '%s <no-reply@%s>' % (site.name, site.domain)
        else:
            return 'no-reply@%s' % site.domain

    def send(self, to_addresses, context={}, attachments=None, headers=None):
        html_body = self.render(context)
        text_body = self.render_txt(context) or striptags(html_body)

        subject = self._render_from_string(self.subject, context)
        if isinstance(to_addresses, (str,unicode)):
            to_addresses = (to_addresses,)

        whitelisted_email_addresses = getattr(settings, 'EMAILTEMPLATES_DEBUG_WHITELIST', [])
        if getattr(settings, 'EMAILTEMPLATES_DEBUG', False):
            # clean non-whitelisted emails from the to_address
            cleaned_to_addresses = []
            for address in to_addresses:
                try:
                    email_domain = address.split('@')[1]
                except IndexError:
                    email_domain = None
                if email_domain in whitelisted_email_addresses or address in whitelisted_email_addresses:
                    cleaned_to_addresses.append(address)
            to_addresses = cleaned_to_addresses

        '''
        msg = EmailMultiAlternatives(subject, text_body, self.visible_from_address(), to_addresses, headers=headers)
        msg.attach_alternative(html_body, "text/html")

        if attachments is not None:
            for attach in attachments:
                msg.attach(*attach)
        status = msg.send()
        '''
        
        status = send_mail(subject, text_body, self.visible_from_address(), to_addresses)
        return status

    def _render_from_string(self, s, context):
        t = Template(s)
        return t.render(Context(context)).encode('ascii', 'ignore')

    @staticmethod
    def send_template(slug, to_address, context={}, attachments=None, headers=None):
        try:
            email_template = EmailTemplate.objects.get(slug=slug)
        except Exception,e:
            print e
            return False
        else:
            return email_template.send(to_address, context, attachments, headers)