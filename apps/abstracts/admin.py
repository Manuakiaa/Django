# Django modules
from django.contrib.admin import ModelAdmin, site


# "Delete selected" makes a real (not soft) delete, so it is turned off
site.disable_action("delete_selected")


class AbstractBaseAdmin(ModelAdmin):
    """Common admin settings for models inherited from AbstractBaseModel."""

    readonly_fields: tuple[str, ...] = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    list_per_page: int = 50
