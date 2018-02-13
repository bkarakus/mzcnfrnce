# coding: utf-8

from django.db import models
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

from mezzanine.pages.models import Page
from mezzanine.core.models import SiteRelated, RichText
from mezzanine.utils.sites import current_site_id, current_request
from mezzanine.utils.views import paginate
from django_countries.fields import CountryField

alphanumeric_regex = r'^[a-zA-Z\.\-\_\ ]*$'
alphanumeric_message = 'Please use only English Alphabet'

alphanumeric = RegexValidator(regex=alphanumeric_regex, message=alphanumeric_message, code='invalid_regex')

class Title(SiteRelated):
    aciklama = models.CharField(u'Açıklama', max_length=50, unique=True)
    
    def __unicode__(self):
        return self.aciklama
    
    class Meta:
        verbose_name = _('Title')
        verbose_name_plural = _('Titles')
        
class Profile(SiteRelated):
    user = models.ForeignKey(User, blank=True, null=True,related_name="profile_list")
    title = models.ForeignKey(Title, null=True)
    name = models.CharField(max_length=100, null=True, validators=[alphanumeric,],help_text=("As you would like it to appear in the "
                                                       "conference program."))
    biography = models.TextField(blank=True, help_text=mark_safe("A little bit about you.  Edit using "
                                                   "<a href='http://warpedvisions.org/projects/"
                                                   "markdown-cheat-sheet/target='_blank'>"
                                                   "Markdown</a>."))
    university = models.CharField(_('University'), validators=[alphanumeric,], max_length=100, null=True)
    department = models.CharField(_('Department'), validators=[alphanumeric,], max_length=100, null=True)
    country = CountryField(_('Country'),max_length=2, default='TR')
    phone = models.CharField(_('Phone'),max_length=20,null=True)
    photo = models.ImageField(upload_to="profile_photos", blank=True)
    in_speakers_page = models.BooleanField(default=False)
    in_participants_page = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
        
    def get_talks_url(self):
        if self.user:
            return reverse('public_usertalks', args=(self.user.username,))
        else:
            url_arg = 'profile-%s' % (self.pk)
            return reverse('public_usertalks', args=(url_arg,))

    def __unicode__(self):
        return unicode(self.name) or u''
        
class ProfilesPage(Page, RichText):
    SPEAKERS = 'S'
    PARTICIPANTS = 'P'
    PROFILE_TYPES = (
        (SPEAKERS, _('Speakers')),
        (PARTICIPANTS, _('Participants')),
    )
    
    profile_type = models.CharField(_(u'Profile Type'), max_length=1, choices=PROFILE_TYPES)
    per_page = models.SmallIntegerField(_(u'Profiles per page'), default=25, help_text=_(u'Number of profiles shown in the page.'))
    
    def get_template_name(self):
        if self.profile_type == ProfilesPage.SPEAKERS:
            return 'pages/speakers.html'
        else:
            return 'pages/participants.html'
        
    def can_add(self, request):
        return False
        
    def profile_list(self):
        request = current_request()
        if self.profile_type == ProfilesPage.SPEAKERS:
            profiles_lst = Profile.objects.filter(in_speakers_page=True)
        else:
            profiles_lst = Profile.objects.filter(in_participants_page=True)
        
        profiles_lst = profiles_lst.annotate(talks_count=Count('author'))
        
        page_num = request.GET.get("page", 1)
            
        profiles = paginate(profiles_lst, page_num, self.per_page, 10)
        
        return profiles
    
    def profile_ids(self):
        from talks.models import Author, Talk, ACCEPTED
        accepted_talk_ids = Talk.objects.filter(status=ACCEPTED).exclude(Q(abstract_pdf='')|Q(abstract_pdf=None)).values_list('id', flat=True)
        profile_ids = Author.objects.filter(talk_id__in=accepted_talk_ids).distinct().values_list('profile_id', flat=True)
        return profile_ids