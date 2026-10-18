# Django modules
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet


class IsDeletedListFilter(SimpleListFilter):
    """Admin filter: deleted / not deleted objects."""

    title = "Is deleted object"
    parameter_name = "is_deleted"

    DELETED_KEY = "deleted"
    NONDELETED_KEY = "non-deleted"

    def lookups(
        self,
        request: WSGIRequest,
        model_admin: ModelAdmin,
    ) -> list[tuple[str, str]]:
        """Options shown in the right sidebar of the admin panel."""
        return [
            (self.DELETED_KEY, "Deleted"),
            (self.NONDELETED_KEY, "Not deleted"),
        ]

    def queryset(self, request: WSGIRequest, queryset: QuerySet) -> QuerySet:
        """Filter queryset by the selected option."""
        if self.value() == self.DELETED_KEY:
            return queryset.filter(deleted_at__isnull=False)
        if self.value() == self.NONDELETED_KEY:
            return queryset.filter(deleted_at__isnull=True)
        return queryset.all()
