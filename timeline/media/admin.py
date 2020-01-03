from django.contrib import admin

from media.models import StatusPost

class StatusPostAdmin(admin.ModelAdmin):
    readonly_fields = ('date_posted',)

admin.site.register(StatusPost, StatusPostAdmin)
