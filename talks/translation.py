from modeltranslation.translator import translator, TranslationOptions

from talks.models import Author

class TranslatedAuthor(TranslationOptions):
    fields = ()

translator.register(Author, TranslatedAuthor)