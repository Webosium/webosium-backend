from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from core.models import Event, Tag

# Register your models here.
def approve_event(modeladmin, request, queryset):
    queryset.update(status='A')

def reject_event(modeladmin, request, queryset):
    queryset.update(status='R')

def archive_event(modeladmin, request, queryset):
    queryset.update(archived=True)

def unarchive_event(modeladmin, request, queryset):
    queryset.update(archived=False)

approve_event.short_description = "Approve events"
reject_event.short_description = "Reject events"
archive_event.short_description = "Archive events"
unarchive_event.short_description = "Uarchive events"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields=('name', 'link', 'date', 'timezone', 'created_by', 'description', 'image', 'image_tag', 'tags', 'status', 'created_at', 'updated_at', 'archived',)
    list_display=('name', 'event_url', 'date', 'timezone', 'image_tag', 'all_tags', 'created_by', 'status','archived',)
    readonly_fields = ('image_tag', 'created_at', 'updated_at',)
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }
    list_filter = ('status', 'tags',)
    actions = (approve_event, reject_event, archive_event, unarchive_event)

    def all_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    def event_url(self, obj):
        return format_html("<a href='{url}' target='_blank'>link to event</a>", url=obj.link)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="150px" />'.format(obj.image.url))
        else:
            return 'No Image'

    image_tag.short_description = 'image'
    all_tags.short_description = 'tags'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields=('name', 'created_by', 'archived',)
    list_display=('name', 'created_by', 'archived', 'created_at', 'updated_at',)
    actions = (archive_event, unarchive_event)