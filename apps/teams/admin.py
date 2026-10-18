# Django modules
from django.contrib.admin import register

# Project modules
from apps.abstracts.admin import AbstractBaseAdmin
from apps.abstracts.filters import IsDeletedListFilter
from apps.teams.models import Team, TeamMembership, JoinRequest, LFGPost


@register(Team)
class TeamAdmin(AbstractBaseAdmin):
    """Team model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "tag",
        "name",
        "game",
        "owner",
        "members_count",
        "deleted_at",
    )
    list_filter: tuple = (
        "game",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "name",
        "tag",
        "owner__nickname",
    )

    def members_count(self, instance: Team) -> int:
        """Number of not deleted members of the team."""
        return instance.teammembership_set.filter(
            deleted_at__isnull=True
        ).count()
    members_count.short_description = "Members"


@register(TeamMembership)
class TeamMembershipAdmin(AbstractBaseAdmin):
    """TeamMembership model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "user",
        "team",
        "is_captain",
        "deleted_at",
    )
    list_filter: tuple = (
        "team",
        "is_captain",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "user__nickname",
        "team__name",
    )
    list_editable: tuple[str, ...] = (
        "is_captain",
    )


@register(JoinRequest)
class JoinRequestAdmin(AbstractBaseAdmin):
    """JoinRequest model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "user",
        "team",
        "is_accepted",
        "created_at",
        "deleted_at",
    )
    list_filter: tuple = (
        "team",
        "is_accepted",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "user__nickname",
        "team__name",
    )
    list_editable: tuple[str, ...] = (
        "is_accepted",
    )


@register(LFGPost)
class LFGPostAdmin(AbstractBaseAdmin):
    """LFGPost model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "author",
        "game",
        "rank_required",
        "is_active",
        "created_at",
        "deleted_at",
    )
    list_filter: tuple = (
        "game",
        "is_active",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "author__nickname",
        "description",
    )
    list_editable: tuple[str, ...] = (
        "is_active",
    )
