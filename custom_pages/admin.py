from copy import deepcopy
from django.contrib import admin

#from mezzanine.forms.admin import FormAdmin
#from mezzanine.forms.models import Form
from mezzanine.core.admin import TabularDynamicInlineAdmin
#from mezzanine.galleries.admin import GalleryAdmin
#from mezzanine.galleries.models import Gallery
from mezzanine.pages.admin import PageAdmin
#from mezzanine.pages.models import RichTextPage

from custom_pages.models import HomePage, Slide

'''
page_fieldsets = deepcopy(PageAdmin.fieldsets)
page_fieldsets[0][1]["fields"].insert(1, "subtitle")
page_fieldsets[0][1]["fields"].insert(2, "image")
PageAdmin.fieldsets = page_fieldsets
GalleryAdmin.fieldsets = page_fieldsets
'''
class SlideInline(TabularDynamicInlineAdmin):
    model = Slide

class HomePageAdmin(PageAdmin):
    inlines = [SlideInline]

#admin.site.unregister(Gallery)
#admin.site.register(Gallery, GalleryAdmin)
#admin.site.unregister(RichTextPage)
#admin.site.register(RichTextPage, PageAdmin)
admin.site.register(HomePage, HomePageAdmin)