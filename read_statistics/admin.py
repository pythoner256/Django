from django.contrib import admin
from.models import ReadNum, ReadDetail


class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['read_num', 'content_type']


class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ['date', 'read_num', 'content_type']


admin.site.register(ReadNum, ReadNumAdmin)
admin.site.register(ReadDetail, ReadDetailAdmin)
