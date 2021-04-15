from django.contrib import admin
from .models import *
# Register your models here.


admin.site.site_header = "Surveyor Admin"
admin.site.site_title = "Surveyor"


class QuestionInline(admin.TabularInline):
    model = Questions
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['title_name']}),
        ('Category', {'fields': ['category']}),
        ('Number of respondants on this survey', {'fields': ['people']})
    ]
    inlines = [QuestionInline]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(User)
admin.site.register(SubmittedSurveys)
admin.site.register(Category)

