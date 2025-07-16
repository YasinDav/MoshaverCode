from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Developer, Guide, SubGuide, ContactUs

admin.site.register(Developer)

admin.site.register(SubGuide)

admin.site.register(ContactUs)


@admin.register(Guide)
class GuideAdmin(SummernoteModelAdmin):
    list_display = ('id', 'guide_name', 'title',)
    search_fields = ('guide_name', 'title', 'description',)
    summernote_fields = ('description',)
