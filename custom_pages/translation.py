from modeltranslation.translator import translator, TranslationOptions
from mezzanine.core.translation import (TranslatedDisplayable,
                                        TranslatedRichText)

from custom_pages.models import HomePage, Slide

class TranslatedHomePage(TranslatedRichText):
    fields = ()

class TranslatedSlide(TranslationOptions):
    fields = ('heading', 'caption',)

translator.register(HomePage, TranslatedHomePage)
translator.register(Slide, TranslatedSlide)