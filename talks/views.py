import json

from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect

from mezzanine.conf import settings

from profiles.models import Profile, User

from talks.models import Talk, Author, ACCEPTED, PENDING
from talks.forms import TalkForm, AuthorFormSet, AuthorFormSetHelper, FullPaperForm

from django.http import Http404, HttpResponse

def get_profile(request, profile_id):
    if request.is_ajax():
        try:
            profile = Profile.objects.get(pk=profile_id)
        except:
            raise Http404
        else:
            if profile.user:
                email = profile.user.email
            else:
                email = ''
            value = {'name': profile.name, 'email': email}
        data = json.dumps(value)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

class EditOwnTalksMixin(object):
    '''Users can edit their own talks as long as the talk is
       "Under Consideration"'''
    def get_object(self, *args, **kwargs):
        object_ = super(EditOwnTalksMixin, self).get_object(*args, **kwargs)
        if object_.can_edit(self.request.user):
            return object_
        else:
            raise PermissionDenied


class LoginRequiredMixin(object):
    '''Must be logged in'''
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class UsersTalks(LoginRequiredMixin, ListView):
    template_name = 'talks/talks.html'
    paginate_by = 25

    def get_queryset(self):
        # self.request will be None when we come here via the static site
        # renderer
        # if (self.request and Talk.can_view_all(self.request.user)):
        #    return Talk.objects.all()
        return Talk.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(UsersTalks, self).get_context_data(**kwargs)
        context['can_submit_fullpaper'] = getattr(settings, 'TALKS_FULLPAPER_SUBMIT_OPEN', False)
        return context
    
class PublicUserTalks(ListView):
    template_name = 'talks/public_talks.html'
    paginate_by = 25
    
    def dispatch(self, request, *args, **kwargs):
        username = kwargs.pop('username')
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
        except:
            profile = None
        
        if profile is None:
            if username.startswith('profile-'):
                try:
                    pk = int(username.replace('profile-',''))
                except:
                    pk = None
                profile = Profile.objects.get(pk=pk)
                    
        if profile is None:
            raise Http404()
        self.profile = profile
        return super(PublicUserTalks, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context =  super(PublicUserTalks, self).get_context_data(**kwargs)
        context.update({'profile': self.profile})
        return context

    def get_queryset(self):
        # self.request will be None when we come here via the static site
        # renderer
        # if (self.request and Talk.can_view_all(self.request.user)):
        #    return Talk.objects.all()
        talk_ids = Author.objects.filter(profile=self.profile).values_list('talk_id', flat=True)
        qs = Talk.objects.filter(id__in=talk_ids, status=ACCEPTED)
        qs = qs.exclude(abstract_pdf=None)
        return qs
    
    def render_to_response(self, context, **response_kwargs):
        talk_count = self.get_queryset().count()
        if talk_count == 0:
            raise Http404()
        elif talk_count == 1:
            talk = self.get_queryset().first()
            if talk.abstract_pdf:
                return redirect(talk.abstract_pdf.url)
        return super(PublicUserTalks, self).render_to_response(context, **response_kwargs)

class TalkView(LoginRequiredMixin, DetailView):
    template_name = 'talks/talk.html'
    model = Talk

    def get_object(self, *args, **kwargs):
        '''Only talk owners can see talks, unless they've been accepted'''
        object_ = super(TalkView, self).get_object(*args, **kwargs)
        if object_.can_view(self.request.user):
            return object_
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(TalkView, self).get_context_data(**kwargs)
        context['can_edit'] = self.object.can_edit(self.request.user)
        return context

class TalkCreate(LoginRequiredMixin, CreateView):
    model = Talk
    form_class = TalkForm
    template_name = 'talks/talk_form.html'
    success_url = reverse_lazy('users_talks')

    def get_context_data(self, **kwargs):
        context = super(TalkCreate, self).get_context_data(**kwargs)
        context['can_submit'] = getattr(settings, 'TALKS_SUBMIT_OPEN', False)
        if self.request.POST:
            context['authors'] = AuthorFormSet(self.request.POST)
            context['helper'] = AuthorFormSetHelper()
        else:
            context['authors'] = AuthorFormSet()
            context['helper'] = AuthorFormSetHelper()
        return context

    def form_valid(self, form):
        if not getattr(settings, 'TALKS_SUBMIT_OPEN', False):
            raise ValidationError  # Should this be SuspiciousOperation?
        # Eaaargh we have to do the work of CreateView if we want to set values
        # before saving
        context = self.get_context_data()
        authors = context['authors']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
        if authors.is_valid():
            authors.instance = self.object
            authors.save()
        return HttpResponseRedirect(self.get_success_url())

class TalkUpdate(LoginRequiredMixin, UpdateView):
    model = Talk
    form_class = TalkForm
    template_name = 'talks/talk_form.html'

    def get_context_data(self, **kwargs):
        context = super(TalkUpdate, self).get_context_data(**kwargs)
        context['can_edit'] = self.object.can_edit(self.request.user)
        if self.request.POST:
            context['authors'] = AuthorFormSet(instance=self.get_object(), data=self.request.POST,)
            context['helper'] = AuthorFormSetHelper()
        else:
            context['authors'] = AuthorFormSet(instance=self.get_object())
            context['helper'] = AuthorFormSetHelper()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        authors = context['authors']
        if authors.is_valid():
            with transaction.atomic():
                form.instance.user = self.request.user
                self.object = form.save()
                authors.instance = self.object
                authors.save()
        else:
            return self.form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())
    
    def post(self, request, *args, **kwargs):
        return UpdateView.post(self, request, *args, **kwargs)
    
class FullPaperSubmit(LoginRequiredMixin, UpdateView):
    model = Talk
    form_class = FullPaperForm
    template_name = 'talks/fullpaper_form.html'
    
    def form_valid(self, form):
        form.instance.fullpaper_status = PENDING
        return super(FullPaperSubmit, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(FullPaperSubmit, self).get_context_data(**kwargs)
        context['can_edit'] = self.object.can_edit_fullpaper(self.request.user)
        context['can_submit_fullpaper'] = getattr(settings, 'TALKS_FULLPAPER_SUBMIT_OPEN', False)
        return context

class TalkDelete(LoginRequiredMixin, DeleteView):
    model = Talk
    template_name = 'talks/talk_delete.html'
    success_url = reverse_lazy('users_talks')
