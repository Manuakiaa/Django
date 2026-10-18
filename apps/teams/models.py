# Django modules
from django.db.models import (
    CharField,
    BooleanField,
    TextField,
    ForeignKey,
    UniqueConstraint,
    PROTECT,
)

# Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.marketplace.models import Game
from apps.users.models import CustomUser


class Team(AbstractBaseModel):
    """Gaming club / clan."""

    NAME_MAX_LEN: int = 70
    TAG_MAX_LEN: int = 10

    name = CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )
    tag = CharField(
        max_length=TAG_MAX_LEN,
        help_text="Short clan tag, e.g. NAVI",
    )
    description = TextField(
        blank=True,
        default="",
    )
    game = ForeignKey(
        to=Game,
        on_delete=PROTECT,
        related_name="teams",
    )
    owner = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="owned_teams",
    )

    def __str__(self) -> str:
        return f"[{self.tag}] {self.name}"


class TeamMembership(AbstractBaseModel):
    """Relationship table between CustomUser and Team."""

    user = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
    )
    team = ForeignKey(
        to=Team,
        on_delete=PROTECT,
    )
    is_captain = BooleanField(
        default=False,
    )

    class Meta:
        """Meta data of the table."""

        constraints = [
            UniqueConstraint(
                fields=("user", "team"),
                name="unique_user_team",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} in {self.team}"


class JoinRequest(AbstractBaseModel):
    """Request of a gamer to join a team."""

    user = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="join_requests",
    )
    team = ForeignKey(
        to=Team,
        on_delete=PROTECT,
        related_name="join_requests",
    )
    message = TextField(
        blank=True,
        default="",
    )
    is_accepted = BooleanField(
        default=False,
    )

    class Meta:
        """Meta data of the table."""

        constraints = [
            UniqueConstraint(
                fields=("user", "team"),
                name="unique_join_request",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.team}"


class LFGPost(AbstractBaseModel):
    """LFG (Looking For Group) post: search for teammates."""

    RANK_MAX_LEN: int = 50

    author = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="lfg_posts",
    )
    game = ForeignKey(
        to=Game,
        on_delete=PROTECT,
        related_name="lfg_posts",
    )
    rank_required = CharField(
        max_length=RANK_MAX_LEN,
        blank=True,
        default="",
    )
    description = TextField()
    is_active = BooleanField(
        default=True,
    )

    class Meta:
        """Meta data of the table."""

        verbose_name = "LFG post"
        verbose_name_plural = "LFG posts"

    def __str__(self) -> str:
        return f"{self.author} looks for {self.game}"
