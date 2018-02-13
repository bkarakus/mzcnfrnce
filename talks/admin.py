# encoding: utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template import Template, Context
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib import messages
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters

from import_export import resources, fields
from import_export.admin import ExportMixin

from mezzanine.core.admin import TabularDynamicInlineAdmin
from talks.models import TalkType, Talk, TalkUrl, Author, TalkSubject
from talks.forms import AuthorForm

csrf_protect_m = method_decorator(csrf_protect)

class TalkResource(resources.ModelResource):
    title = fields.Field(column_name=u'Title')
    talk_type = fields.Field(column_name=u'Talk Type')
    talk_subject = fields.Field(column_name=u'Talk Subject')
    presenter = fields.Field(column_name=u'Presenter')
    first_author = fields.Field(column_name=u'1st Author')
    second_author = fields.Field(column_name=u'2nd Author')
    third_author = fields.Field(column_name=u'3rd Author')
    
    class Meta:
        model = Talk
        export_order = ('id','talk_type', 'talk_subject', 'title', 'presenter', 'first_author', 'second_author', 'third_author')
        fields = ('id','talk_type', 'talk_subject', 'title', 'presenter', 'first_author', 'second_author', 'third_author')
    
    def dehydrate_title(self, obj):
        return obj.title
    
    def dehydrate_talk_type(self, obj):
        return obj.talk_type.name
    
    def dehydrate_talk_subject(self, obj):
        return obj.talk_subject.name
    
    def dehydrate_presenter(self, obj):
        presenter = obj.authors.filter(is_presenter=True).first()
        if not presenter:
            presenter = obj.user.profile_list.first()
        
        if presenter:
            return presenter.name
        
    def get_author(self, obj, index):
        try:
            author = obj.authors.all()[index]
        except:
            return ''
        else:
            return author.name
    
    def dehydrate_first_author(self, obj):
        return self.get_author(obj, 0)
    
    def dehydrate_second_author(self, obj):
        return self.get_author(obj, 1)
    
    def dehydrate_third_author(self, obj):
        return self.get_author(obj, 2)
    
        
class ScheduleListFilter(admin.SimpleListFilter):
    title = _('in schedule')
    parameter_name = 'schedule'

    def lookups(self, request, model_admin):
        return (
            ('in', _('Allocated to schedule')),
            ('out', _('Not allocated')),
            )

    def queryset(self, request, queryset):
        if self.value() == 'in':
            return queryset.filter(scheduleitem__isnull=False)
        elif self.value() == 'out':
            return queryset.filter(scheduleitem__isnull=True)
        return queryset

class TalkUrlAdmin(admin.ModelAdmin):
    list_display = ('description', 'talk', 'url')

class TalkUrlInline(TabularDynamicInlineAdmin):
    model = TalkUrl
    
class AuthorInline(TabularDynamicInlineAdmin):
    model = Author
    form = AuthorForm
    extra = 3

class TalkAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('title', 'talk_type', 'talk_subject', 'presenter', 'talk_actions',)
    list_filter = ('talk_type', 'talk_subject', 'status', 'aippaper_status',)
    search_fields = ('title', )
    readonly_fields = ('notes',)
    inlines = [AuthorInline, ]
    resource_class = TalkResource
    
    def presenter(self, obj):
        presenter = obj.authors.filter(is_presenter=True).first()
        if not presenter:
            presenter = obj.user.profile_list.first()
        
        if presenter:
            return presenter.name
    
    class Media:
        js = (
            'js/admin/talks_admin.js',
        )
    
    def get_urls(self):
        from django.conf.urls import patterns
        return patterns('',
            (r'^(?P<object_id>\d+)/(?P<paper_type>short-abstract|aippaper)/(?P<status>accept|reject)/$', self.admin_site.admin_view(self.accept_or_reject)),
        ) + super(TalkAdmin, self).get_urls()
    
    def talk_actions(self, obj):
        template = Template("""
        {% load i18n %}
        <select class="addlist" style="width:100px;">
            <option value="">Select ...</option>
            <optgroup label="{% trans 'Short Abstract' %}">
                <option value="{{ obj.abstract.url }}">View LaTeX File</option>
                {% if obj.abstract_pdf %}
                <option value="{{ obj.abstract_pdf.url }}">View PDF File</option>
                {% endif %}
                {% if obj.pending %}
                <option value="{{ obj.pk }}/short-abstract/accept/">{% trans 'Accept' %} ...</option>
                <option value="{{ obj.pk }}/short-abstract/reject/">{% trans 'Reject' %} ...</option>
                {% endif %}
            </optgroup>
            <optgroup label="{% trans 'AIP Paper' %}">
                {% if obj.aippaper %}
                <option value="{{ obj.aippaper.url }}">View ZIP File</option>
                {% endif %}
                {% if obj.aippaper_pdf %}
                <option value="{{ obj.aippaper_pdf.url }}">View PDF File</option>
                {% endif %}
                {% if obj.aippaper_pending %}
                <option value="{{ obj.pk }}/aippaper/accept/">{% trans 'Accept' %} ...</option>
                <option value="{{ obj.pk }}/aippaper/reject/">{% trans 'Reject' %} ...</option>
                {% endif %}
            </optgroup>
        </select>
        """)
        context = Context({
            'obj': obj,
        })
        html = template.render(context)
        return html
    
    talk_actions.mark_safe = True
    talk_actions.allow_tags = True
    talk_actions.short_description = u'Actions'
    
    @csrf_protect_m
    def accept_or_reject(self, request, object_id, paper_type, status, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, object_id)

        if obj is None:
            raise Http404(
                _('%(name)s object with primary key %(key)r does not exist.') %
                    {'name': force_text(opts.verbose_name), 'key': escape(object_id)}
            )

        if request.POST:  # The user has already confirmed the deletion.
            obj_display = force_text(obj)
            
            if paper_type == 'short-abstract':
                email_send = obj.abstract_accept_or_reject(status)
            else:
                email_send = obj.aippaper_accept_or_reject(status)
                
            if email_send:
                self.message_user(request, _(u"Accept/Reject email has been sent."), messages.SUCCESS)
            else:
                self.message_user(request, _(u"Accept/Reject email could not be sent"), messages.ERROR)

            if self.has_change_permission(request, None):
                post_url = reverse('admin:%s_%s_changelist' %
                                   (opts.app_label, opts.model_name),
                                   current_app=self.admin_site.name)
                preserved_filters = self.get_preserved_filters(request)
                post_url = add_preserved_filters(
                    {'preserved_filters': preserved_filters, 'opts': opts}, post_url
                )
            else:
                post_url = reverse('admin:index',
                                   current_app=self.admin_site.name)
            return HttpResponseRedirect(post_url)

        object_name = force_text(opts.verbose_name)

        title = _("Are you sure?")

        context = {
            "title": title,
            "object_name": object_name,
            "object": obj,
            "opts": opts,
            "app_label": app_label,
            'preserved_filters': self.get_preserved_filters(request),
            "button_value": "%s(%s)" % (paper_type, status),
        }
        context.update(extra_context or {})

        return TemplateResponse(request, ["admin/%s/accept_or_reject.html" % (app_label),], 
                                context, current_app=self.admin_site.name)
        
class TalkSubjectAdmin(admin.ModelAdmin):
    #sortable_field_name = "order"
    list_display = ('name', 'order', )
    list_editable = ('order',)

admin.site.register(Talk, TalkAdmin)
admin.site.register(TalkType)
admin.site.register(TalkSubject, TalkSubjectAdmin)
admin.site.register(TalkUrl, TalkUrlAdmin)
