from django.contrib import admin

"""L'admin Django par défaut suffit pour User. Pas de modèle custom ici."""


from .models import DataRequest


@admin.register(DataRequest)
class DataRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "export_format", "requested_at", "responded_at", "file_hash")
    list_filter = ("status", "export_format", "requested_at")
    search_fields = ("user__email", "user__username", "file_hash")
    readonly_fields = ("requested_at", "responded_at", "file_hash")
