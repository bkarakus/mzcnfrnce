import os
#import magic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible

from mezzanine.core.models import SiteRelated, Ownable, Orderable
from mezzanine.conf import settings as mezzanine_settings

from utils.files import get_abstracts_path
from utils.files import get_fullpapers_path

from dbemail.models import EmailTemplate
from profiles.models import Profile

# constants to make things clearer elsewhere
ACCEPTED = 'A'
PENDING = 'P'
REJECTED = 'R'
EMPTY = 'E'

'''
def validate_file_extension(value):
    content_types = mezzanine_settings.TALKS_FILE_CONTENT_TYPES
    content_types = content_types.split(',')
    if content_types:
        content_type = magic.from_buffer(value.file.read(), mime=True)
        if content_type not in content_types:
            raise ValidationError(mezzanine_settings.TALKS_FILE_CONTENT_TYPE_ERROR_MESSAGE)
        
def validate_pdf_file(value):
    content_type = magic.from_buffer(value.file.read(), mime=True)
    if content_type != 'application/pdf':
        raise ValidationError(u'Unsupported file type.')
        
def validate_zip_file(value):
    ZIP_CONTENT_TYPES=['application/x-compressed', 'application/x-zip-compressed',
                       'application/zip', 'multipart/x-zip', 'application/x-rar']
    content_type = magic.from_buffer(value.file.read(), mime=True)
    if content_type not in ZIP_CONTENT_TYPES:
        raise ValidationError(u'Only .zip and .rar files are allowed.')
'''

def validate_file_extension(value):
    extensions = mezzanine_settings.TALKS_FILE_EXTENSIONS
    extensions = extensions.replace(' ', '')
    extensions = extensions.split(',')
    if extensions:
        file_name, ext = os.path.splitext(value.file.name)
        if ext not in extensions:
            raise ValidationError(mezzanine_settings.TALKS_FILE_CONTENT_TYPE_ERROR_MESSAGE)
        
def validate_pdf_file(value):
    file_name, ext = os.path.splitext(value.file.name)
    if ext not in ['.pdf', ]:
        raise ValidationError(u'Unsupported file type.')
        
def validate_zip_file(value):
    file_name, ext = os.path.splitext(value.file.name)
    if ext not in ['.zip', '.rar']:
        raise ValidationError(u'Only .zip and .rar files are allowed.')

@python_2_unicode_compatible
class TalkType(SiteRelated):
    """A type of talk."""
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)

    def __str__(self):
        return u'%s' % (self.name,)
    
@python_2_unicode_compatible
class TalkSubject(SiteRelated):
    """A type of talk."""
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('order', 'name')
        
    def __str__(self):
        return u'%s' % (self.name,)

@python_2_unicode_compatible
class Talk(SiteRelated, Ownable):
    class Meta:
        permissions = (
            ("view_all_talks", "Can see all talks"),
        )

    TALK_STATUS = (
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Not Accepted'),
        (PENDING, 'Under Consideration'),
        (EMPTY, 'Not Submitted')
    )
    
    talk_type = models.ForeignKey(TalkType, null=True)
    talk_subject = models.ForeignKey(TalkSubject, null=True)

    title = models.CharField(max_length=1024)

    abstract = models.FileField(_('File'), max_length=255, upload_to=get_abstracts_path, validators=[validate_file_extension])
    abstract_pdf = models.FileField(_('File (PDF)'), max_length=255, blank=True, null=True, upload_to=get_abstracts_path,validators=[validate_pdf_file])
    notes = models.TextField(
        null=True, blank=True,
        help_text=_("Any notes for the conference organisers?"))

    status = models.CharField(max_length=1, choices=TALK_STATUS,
                              default=PENDING)
    
    fullpaper = models.FileField(_('Full Paper'), null=True, blank=True, max_length=255, upload_to=get_fullpapers_path, validators=[validate_pdf_file],
                                help_text='Only .pdf files')
    fullpaper_pdf = models.FileField(_('Full Paper (PDF)'), max_length=255, blank=True, null=True, upload_to=get_fullpapers_path,validators=[validate_pdf_file])
    fullpaper_status = models.CharField(max_length=1, choices=TALK_STATUS,
                              default=EMPTY)

    def __str__(self):
        return u'%s: %s' % (self.user, self.title)

    def get_absolute_url(self):
        return reverse('talk_detail', args=(self.pk,))

    def get_author_contact(self):
        email = self.corresponding_author.email
        profile = self.corresponding_author
        if profile.phone:
            contact = profile.phone
        else:
            # Should we wrap this in a span for styling?
            contact = 'NO CONTACT INFO'
        return '%s - %s' % (email, contact)
    get_author_contact.short_description = 'Contact Details'

    def get_author_name(self):
        return '%s (%s)' % (self.corresponding_author,
                            self.corresponding_author.get_full_name())

    get_author_name.admin_order_field = 'corresponding_author'
    get_author_name.short_description = 'Corresponding Author'

    def get_author_display_name(self):
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        return self.user.username
    
    def get_authors_display(self):
        return ', '.join([author.name for author in self.authors.all()])
        
    def get_in_schedule(self):
        if self.scheduleitem_set.all():
            return True
        return False

    get_in_schedule.short_description = 'Added to schedule'
    get_in_schedule.boolean = True

    def has_url(self):
        """Test if the talk has urls associated with it"""
        if self.talkurl_set.all():
            return True
        return False

    has_url.boolean = True

    # Helpful properties for the templates
    accepted = property(fget=lambda x: x.status == ACCEPTED)
    pending = property(fget=lambda x: x.status == PENDING)
    rejected = property(fget=lambda x: x.status == REJECTED)
    
    # Helpful properties for the templates
    fullpaper_accepted = property(fget=lambda x: x.fullpaper_status == ACCEPTED)
    fullpaper_pending = property(fget=lambda x: x.fullpaper_status == PENDING)
    fullpaper_rejected = property(fget=lambda x: x.fullpaper_status == REJECTED)
    fullpaper_empty = property(fget=lambda x: x.fullpaper_status == EMPTY)

    def can_view(self, user):
        if user.has_perm('talks.view_all_talks'):
            return True
        if self.user.pk == user.pk:
            return True
        if self.accepted:
            return True
        return False

    @classmethod
    def can_view_all(cls, user):
        return user.has_perm('talks.view_all_talks')

    def can_edit(self, user):
        #if user.has_perm('talks.change_talk'):
        #    return True
        if self.pending:
            if self.user.pk == user.pk:
                return True
        return False
    
    def can_edit_fullpaper(self, user):
        can_submit_fullpaper = getattr(mezzanine_settings, 'TALKS_FULLPAPER_SUBMIT_OPEN', False)
        print can_submit_fullpaper
        if not can_submit_fullpaper:
            return False
        if user.has_perm('talks.change_talk'):
            return True
        if self.fullpaper_empty or self.fullpaper_pending:
            if self.user.pk == user.pk:
                return True
        return False
    
    def abstract_status_class(self):
        if self.pending:
            return 'label-info'
        elif self.accepted:
            return 'label-success'
        elif self.rejected:
            return 'label-danger'
        
    def fullpaper_status_class(self):
        if self.fullpaper_pending:
            return 'label-info'
        elif self.fullpaper_accepted:
            return 'label-success'
        elif self.fullpaper_rejected:
            return 'label-danger'
        elif self.fullpaper_empty:
            return 'label-warning'
        
    def abstract_accept_or_reject(self, status):
        if status == 'accept':
            self.status = ACCEPTED
        elif status == 'reject':
            self.status = REJECTED
            
        self.save()
        
        if mezzanine_settings.TALKS_SEND_ACCEPT_REJECT_MAIL:
            template_slug = status
            to_address = self.user.email
            context = {'user': self.user, 'talk': self,}
            return EmailTemplate.send_template(template_slug, to_address, context,)
        return True
    
    def fullpaper_accept_or_reject(self, status):
        if status == 'accept':
            self.fullpaper_status = ACCEPTED
        elif status == 'reject':
            self.fullpaper_status = REJECTED
            
        self.save()
        
        if mezzanine_settings.TALKS_SEND_ACCEPT_REJECT_MAIL:
            template_slug = 'fullpaper-%s' % status
            to_address = self.user.email
            context = {'user': self.user, 'talk': self,}
            return EmailTemplate.send_template(template_slug, to_address, context,)
        return True
'''
@python_2_unicode_compatible
class fullpaper(SiteRelated, Ownable):
    TALK_STATUS = (
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Not Accepted'),
        (PENDING, 'Under Consideration'),
    )
    
    talk = models.ForeignKey(Talk)

    fullpaper = models.FileField(_('File'), max_length=255, upload_to=get_abstracts_path, validators=[validate_zip_file],
                                help_text='Only .zip or .rar files')
    fullpaper_pdf = models.FileField(_('File (PDF)'), max_length=255, blank=True, null=True, upload_to=get_abstracts_path,validators=[validate_pdf_file])
    status = models.CharField(max_length=1, choices=TALK_STATUS,
                              default=PENDING)

    def __str__(self):
        return u'%s: %s' % (self.user, self.title)

    def get_absolute_url(self):
        return reverse('fullpaper_detail', args=(self.pk,))
    
    accepted = property(fget=lambda x: x.status == ACCEPTED)
    pending = property(fget=lambda x: x.status == PENDING)
    reject = property(fget=lambda x: x.status == REJECTED)
'''

class Author(SiteRelated, Orderable):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    profile = models.ForeignKey(Profile, blank=True, null=True)
    name = models.CharField(_('Name'),max_length=100)
    email = models.EmailField(_('email address'), null=True)
    talk = models.ForeignKey(Talk, related_name='authors')
    is_presenter = models.BooleanField(default=False)
        
    def save(self, update_site=False, *args, **kwargs):
        save = True
        if self.profile:
            if self.talk.authors.exclude(pk=self.pk).filter(profile=self.profile):
                save = False
            self.name = self.profile.name
            try:
                self.email = self.profile.user.email
            except:
                pass
        if save:
            super(Author, self).save(update_site=update_site, *args, **kwargs)

class TalkUrl(SiteRelated):
    """An url to stuff relevant to the talk - videos, slides, etc.

       Note that these are explicitly not intended to be exposed to the
       user, but exist for use by the conference organisers."""

    description = models.CharField(max_length=256)
    url = models.URLField()
    talk = models.ForeignKey(Talk)