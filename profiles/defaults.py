from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

register_setting(
    name="SITE_BANNER",
    label=_("site banner"),
    description=_("Site banner"),
    editable=True,
    default="",
    translatable=True,
)

register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=("SITE_BANNER", ),
    append=True,
)