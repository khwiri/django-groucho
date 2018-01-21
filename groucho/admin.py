from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count
from django.db.models.functions import TruncDay
from groucho.models import AttemptUser, AttemptSource, Configuration, ProtectedUser, SourceSummary

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

@admin.register(ProtectedUser)
class ProtectedUserAdmin(admin.ModelAdmin):
    pass

@admin.register(SourceSummary)
class SourceSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/source_summary.html'

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        source_queryset = AttemptSource.objects.all()
        response.context_data['summary'] = source_queryset.values('ip').annotate(Count('ip')).order_by('-ip__count')
        response.context_data['history'] = AttemptSource.objects.annotate(day=TruncDay('created')).values('day').annotate(Count('day')).order_by('day')[:20]
        response.context_data['summary_total'] = source_queryset.count()
        return response