# Django modules
from django.contrib.admin import register

# Project modules
from apps.abstracts.admin import AbstractBaseAdmin
from apps.abstracts.filters import IsDeletedListFilter
from apps.reviews_ratings.models import Review, Report, KarmaVote


@register(Review)
class ReviewAdmin(AbstractBaseAdmin):
    """Review model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "author",
        "target",
        "rating",
        "created_at",
        "deleted_at",
    )
    list_filter: tuple = (
        "rating",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "author__nickname",
        "target__nickname",
        "text",
    )


@register(Report)
class ReportAdmin(AbstractBaseAdmin):
    """Report model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "reporter",
        "reported_user",
        "is_resolved",
        "created_at",
        "deleted_at",
    )
    list_filter: tuple = (
        "is_resolved",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "reporter__nickname",
        "reported_user__nickname",
        "reason",
    )
    list_editable: tuple[str, ...] = (
        "is_resolved",
    )


@register(KarmaVote)
class KarmaVoteAdmin(AbstractBaseAdmin):
    """KarmaVote model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "voter",
        "target",
        "is_positive",
        "deleted_at",
    )
    list_filter: tuple = (
        "is_positive",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "voter__nickname",
        "target__nickname",
    )
