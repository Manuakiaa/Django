# Python modules
from decimal import Decimal

# Django modules
from django.db.models import (
    CharField,
    BooleanField,
    TextField,
    DecimalField,
    ForeignKey,
    UniqueConstraint,
    PROTECT,
)

# Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.users.models import CustomUser


class Game(AbstractBaseModel):
    """Game category (CS2, Dota 2, Valorant...)."""

    NAME_MAX_LEN: int = 70

    name = CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class Listing(AbstractBaseModel):
    """Offer to sell or trade an in-game item or account."""

    TITLE_MAX_LEN: int = 200
    PRICE_MAX_DIGITS: int = 10
    PRICE_DECIMAL_PLACES: int = 2
    PRICE_DEFAULT_VALUE: Decimal = Decimal("0.00")

    seller = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="listings",
    )
    game = ForeignKey(
        to=Game,
        on_delete=PROTECT,
        related_name="listings",
    )
    title = CharField(
        max_length=TITLE_MAX_LEN,
    )
    description = TextField(
        blank=True,
        default="",
    )
    price = DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=PRICE_DEFAULT_VALUE,
    )
    is_account = BooleanField(
        default=False,
        verbose_name="Is game account",
        help_text="Unchecked means in-game item",
    )
    is_trade = BooleanField(
        default=False,
        verbose_name="Is trade",
        help_text="Unchecked means sale for money",
    )
    is_active = BooleanField(
        default=True,
    )

    def __str__(self) -> str:
        return self.title


class DealStatus(AbstractBaseModel):
    """Deal status (Pending, Paid, Completed, Cancelled...)."""

    NAME_MAX_LEN: int = 50

    name = CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    class Meta:
        """Meta data of the table."""

        verbose_name = "Deal status"
        verbose_name_plural = "Deal statuses"

    def __str__(self) -> str:
        return self.name


class Deal(AbstractBaseModel):
    """Deal between a buyer and a seller of the listing."""

    PRICE_MAX_DIGITS: int = 10
    PRICE_DECIMAL_PLACES: int = 2

    listing = ForeignKey(
        to=Listing,
        on_delete=PROTECT,
        related_name="deals",
    )
    buyer = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="purchases",
    )
    status = ForeignKey(
        to=DealStatus,
        on_delete=PROTECT,
        related_name="deals",
    )
    final_price = DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
    )

    class Meta:
        """Meta data of the table."""

        constraints = [
            UniqueConstraint(
                fields=("listing", "buyer"),
                name="unique_listing_buyer",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.listing} -> {self.buyer}"
