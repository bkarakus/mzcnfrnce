# encoding: utf-8
from mezzanine.conf import register_setting

register_setting(
    name="SITE_ADDRESS",
    label=u"Adres",
    description=u"#Adres_1|Adres_2|Posta Kodu İlçe/il# formatında giriniz",
    editable=True,
    default='Adres_1|Adres_2|Posta Kodu İlçe/il'
)

register_setting(
    name="SITE_PHONE",
    label=u"Telefon",
    description=u"Telefon numarası",
    editable=True,
    default='+90 --- -- --'
)

register_setting(
    name="SITE_FAX",
    label=u"FAX",
    description=u"Fax numarası",
    editable=True,
    default='+90 --- -- --'
)

register_setting(
    name="SITE_EMAIL",
    label=u"Email",
    description=u"",
    editable=True,
    default=''
)

register_setting(
    name="SITE_GOOGLE_MAP",
    label=u"Google Map",
    description=u"",
    editable=True,
    default=""
)

register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=("Sequence of setting names available within templates."),
    editable=False,
    default=("SITE_ADDRESS", "SITE_PHONE",
             "SITE_FAX", "SITE_EMAIL",
             "SITE_GOOGLE_MAP",),
    append=True,
)