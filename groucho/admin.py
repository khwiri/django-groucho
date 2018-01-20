from django.contrib import admin
from django.contrib.admin import AdminSite
from groucho.models import AttemptUser, AttemptSource, Configuration

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """
        Defining this method so that the admin interface doesn't allow for
        additional configuration records to be created.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(AttemptUser)
class AttemptUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'created', 'exists']


@admin.register(AttemptSource)
class AttemptSourceAdmin(admin.ModelAdmin):
    list_display = ['ip', 'credentials']