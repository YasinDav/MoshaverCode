from django.contrib import admin

from .models import Consult, Question


# admin.site.register(Consult)
# admin.site.register(Question)
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'consult', 'created_date', 'question', 'answer',)
    list_filter = ('type', 'consult', 'created_date',)
    search_fields = ('type', 'consult', 'answer', 'question',)
    date_hierarchy = 'created_date'


@admin.register(Consult)
class ConsultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_date', 'updated_date', 'status',)
    list_filter = ('user', 'updated_date', 'created_date', 'status',)
