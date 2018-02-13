from modeltranslation.translator import translator, TranslationOptions
from mezzanine.core.translation import (TranslatedDisplayable,
                                        TranslatedRichText)

from profiles.models import ProfilesPage, Title

class TranslatedProfilesPage(TranslatedRichText):
    fields = ()
    
class TranslatedTitle(TranslationOptions):
    fields = ('aciklama',)
    
translator.register(ProfilesPage, TranslatedProfilesPage)
translator.register(Title, TranslatedTitle)