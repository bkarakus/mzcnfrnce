from django.conf.urls import patterns, url

from talks.views import (
    TalkCreate, TalkDelete, TalkUpdate, TalkView, UsersTalks, FullPaperSubmit, get_profile, PublicUserTalks)

urlpatterns = patterns(
    '',
    url(r'^$', UsersTalks.as_view(), name='users_talks'),
    url(r'^page/(?P<page>\d+)$', UsersTalks.as_view(),
        name='users_talks_page'),
    url(r'^new/$', TalkCreate.as_view(), name='talk_submit'),
    url(r'^(?P<pk>\d+)/$', TalkView.as_view(), name='talk_detail'),
    url(r'^(?P<pk>\d+)/edit/$', TalkUpdate.as_view(),
        name='talk_edit'),
    url(r'^(?P<pk>\d+)/delete/$', TalkDelete.as_view(),
        name='talk_delete'),
    url(r'^(?P<pk>\d+)/fullpaper/$', FullPaperSubmit.as_view(),
        name='talk_submit_fullpaper'),
    url(r'^get-profile/(?P<profile_id>\d+)/$', get_profile,
        name='get_profile'),
    url(r'^accepted/(?P<username>[\w.@+-]+)/$', PublicUserTalks.as_view(), name='public_usertalks'),
)
