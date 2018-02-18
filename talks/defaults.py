# encoding: utf-8

from __future__ import unicode_literals
from datetime import date
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

register_setting(
    name="TALKS_SUBMIT_OPEN",
    label=_("Talks Submit Open"),
    description=_("true by default."),
    editable=True,
    default=True,
)

register_setting(
    name="TALKS_FULLPAPER_SUBMIT_OPEN",
    label=_("Talks Full Paper Submit Open"),
    description=_("true by default."),
    editable=True,
    default=True,
)

register_setting(
    name="TALKS_FILE_CONTENT_TYPES",
    label=_("Abstract File Content Types"),
    description=_("Birden fazla içerik tipini virgülle ayırınız. http://www.sitepoint.com/web-foundations/mime-types-complete-list/"),
    editable=True,
    default='application/x-tex, text/x-tex',
)

register_setting(
    name="TALKS_FILE_EXTENSIONS",
    label=_("Abstract File Extensions"),
    description=_("Birden fazla dosya uzantısını virgulle ayırınız."),
    editable=True,
    default='.tex',
)

register_setting(
    name="TALKS_FILE_CONTENT_TYPE_ERROR_MESSAGE",
    label=_("Content Type Error Message"),
    description=_("Özet Dosyası istenilen formatta olmadığında gösterilecek mesaj."),
    editable=True,
    default='Only tex format is allowed.',
)

register_setting(
    name="TALKS_SEND_ACCEPT_REJECT_MAIL",
    label=_("Send accept or reject mail"),
    description=_("Send accept or reject mail"),
    editable=True,
    default=True,
)