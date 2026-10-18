# Django modules
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest

# Project modules
from apps.abstracts.admin import AbstractBaseAdmin
from apps.abstracts.filters import IsDeletedListFilter
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import CustomUser, GameRank


@register(CustomUser)
class CustomUserAdmin(AbstractBaseAdmin, UserAdmin):
    """CustomUser model admin configuration class."""

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display: tuple[str, ...] = (
        "id",
        "email",
        "nickname",
        "discord_id",
        "karma",
        "is_staff",
        "is_active",
        "deleted_at",
    )
    list_display_links: tuple[str, ...] = (
        "id",
        "email",
    )
    list_filter: tuple = (
        "is_staff",
        "is_active",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "id",
        "email",
        "nickname",
        "discord_id",
        "steam_id",
    )
    ordering: tuple[str, ...] = (
        "id",
    )
    filter_horizontal: tuple[str, ...] = (
        "groups",
        "user_permissions",
    )
    readonly_fields: tuple[str, ...] = (
        "id",
        "karma",
        "last_login",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    fieldsets: tuple = (
        (
            "General information",
            {
                "fields": (
                    "id",
                    ("email", "nickname"),
                    "password",
                    "avatar_url",
                    "bio",
                    "karma",
                )
            },
        ),
        (
            "Gaming accounts",
            {
                "fields": (
                    ("discord_id", "steam_id"),
                    "steam_trade_link",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    ("is_staff", "is_active", "is_superuser"),
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Date and time information",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            },
        ),
    )
    add_fieldsets: tuple = (
        (
            None,
            {
                "fields": ("email", "nickname", "password1", "password2"),
            },
        ),
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: CustomUser | None = None,
    ) -> tuple[str, ...]:
        """Email can not be changed after creation."""
        if obj:
            return ("email",) + self.readonly_fields
        return self.readonly_fields

    def karma(self, instance: CustomUser) -> int:
        """Karma of the gamer (see CustomUser.karma)."""
        return instance.karma
    karma.short_description = "Karma"


@register(GameRank)
class GameRankAdmin(AbstractBaseAdmin):
    """GameRank model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "user",
        "game_name",
        "rank",
        "deleted_at",
    )
    list_filter: tuple = (
        "game_name",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "user__nickname",
        "game_name",
        "rank",
    )
    list_editable: tuple[str, ...] = (
        "rank",
    )
