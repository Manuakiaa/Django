# Django modules
from django.db.models import (
    BooleanField,
    TextField,
    PositiveIntegerField,
    ForeignKey,
    UniqueConstraint,
    PROTECT,
)

# Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.users.models import CustomUser


class Review(AbstractBaseModel):
    """Review about a gamer or a seller."""

    RATING_DEFAULT_VALUE: int = 5

    author = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="written_reviews",
    )
    target = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="received_reviews",
    )
    rating = PositiveIntegerField(
        default=RATING_DEFAULT_VALUE,
        help_text="From 1 to 5",
    )
    text = TextField(
        blank=True,
        default="",
    )

    class Meta:
        """Meta data of the table."""

        constraints = [
            UniqueConstraint(
                fields=("author", "target"),
                name="unique_author_target_review",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.author} -> {self.target}: {self.rating}"


class Report(AbstractBaseModel):
    """Complaint about a gamer (cheating, scam, toxicity...)."""

    reporter = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="sent_reports",
    )
    reported_user = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="received_reports",
    )
    reason = TextField()
    is_resolved = BooleanField(
        default=False,
    )

    def __str__(self) -> str:
        return f"{self.reporter} reported {self.reported_user}"


class KarmaVote(AbstractBaseModel):
    """Plus or minus to the karma of a gamer's profile."""

    voter = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="given_karma_votes",
    )
    target = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="karma_votes",
    )
    is_positive = BooleanField(
        default=True,
        help_text="Checked is +1, unchecked is -1",
    )

    class Meta:
        """Meta data of the table."""

        constraints = [
            UniqueConstraint(
                fields=("voter", "target"),
                name="unique_voter_target_karma",
            ),
        ]

    def __str__(self) -> str:
        sign: str = "+1" if self.is_positive else "-1"
        return f"{self.voter} -> {self.target}: {sign}"
