# Django modules
from django.contrib.admin import register

# Project modules
from apps.abstracts.admin import AbstractBaseAdmin
from apps.abstracts.filters import IsDeletedListFilter
from apps.marketplace.models import Game, Listing, DealStatus, Deal


@register(Game)
class GameAdmin(AbstractBaseAdmin):
    """Game model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "name",
        "listings_count",
        "deleted_at",
    )
    list_filter: tuple = (
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "name",
    )

    def listings_count(self, instance: Game) -> int:
        """Number of not deleted listings of the game."""
        return instance.listings.filter(deleted_at__isnull=True).count()
    listings_count.short_description = "Listings"


@register(Listing)
class ListingAdmin(AbstractBaseAdmin):
    """Listing model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "title",
        "game",
        "seller",
        "price",
        "is_account",
        "is_trade",
        "is_active",
        "deleted_at",
    )
    list_filter: tuple = (
        "game",
        "is_account",
        "is_trade",
        "is_active",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "title",
        "description",
        "seller__nickname",
    )
    list_editable: tuple[str, ...] = (
        "price",
        "is_active",
    )


@register(DealStatus)
class DealStatusAdmin(AbstractBaseAdmin):
    """DealStatus model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "name",
        "deleted_at",
    )
    list_filter: tuple = (
        IsDeletedListFilter,
    )


@register(Deal)
class DealAdmin(AbstractBaseAdmin):
    """Deal model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "listing",
        "buyer",
        "status",
        "final_price",
        "created_at",
        "deleted_at",
    )
    list_filter: tuple = (
        "status",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "listing__title",
        "buyer__nickname",
    )
    list_editable: tuple[str, ...] = (
        "status",
    )
