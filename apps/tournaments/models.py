# Python modules
from decimal import Decimal

# Django modules
from django.db.models import (
    CharField,
    BooleanField,
    TextField,
    DateTimeField,
    DecimalField,
    PositiveIntegerField,
    ForeignKey,
    UniqueConstraint,
    PROTECT,
)

# Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.marketplace.models import Game
from apps.teams.models import Team
from apps.users.models import CustomUser


class Tournament(AbstractBaseModel):
    """Tournament with a bracket of matches."""

    NAME_MAX_LEN: int = 100
    PRIZE_MAX_DIGITS: int = 12
    PRIZE_DECIMAL_PLACES: int = 2
    PRIZE_DEFAULT_VALUE: Decimal = Decimal("0.00")
    MAX_TEAMS_DEFAULT_VALUE: int = 8

    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    description = TextField(
        blank=True,
        default="",
    )
    game = ForeignKey(
        to=Game,
        on_delete=PROTECT,
        related_name="tournaments",
    )
    organizer = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT,
        related_name="organized_tournaments",
    )
    start_date = DateTimeField()
    prize_pool = DecimalField(
        max_digits=PRIZE_MAX_DIGITS,
        decimal_places=PRIZE_DECIMAL_PLACES,
        default=PRIZE_DEFAULT_VALUE,
    )
    max_teams = PositiveIntegerField(
        default=MAX_TEAMS_DEFAULT_VALUE,
    )
    is_finished = BooleanField(
        default=False,
    )

    def __str__(self) -> str:
        return self.name


class TournamentRegistration(AbstractBaseModel):
    """Registration of a team for a tournament."""

    tournament = ForeignKey(
        to=Tournament,
        on_delete=PROTECT,
    )
    team = ForeignKey(
        to=Team,
        on_delete=PROTECT,
    )
    is_approved = BooleanField(
        default=False,
    )

    class Meta:
        """Meta data of the table."""

        constraints = [
            UniqueConstraint(
                fields=("tournament", "team"),
                name="unique_tournament_team",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.team} in {self.tournament}"


class Match(AbstractBaseModel):
    """Match between two teams in a tournament (schedule and result)."""

    ROUND_DEFAULT_VALUE: int = 1
    SCORE_DEFAULT_VALUE: int = 0

    tournament = ForeignKey(
        to=Tournament,
        on_delete=PROTECT,
        related_name="matches",
    )
    team_one = ForeignKey(
        to=Team,
        on_delete=PROTECT,
        related_name="matches_as_team_one",
    )
    team_two = ForeignKey(
        to=Team,
        on_delete=PROTECT,
        related_name="matches_as_team_two",
    )
    round_number = PositiveIntegerField(
        default=ROUND_DEFAULT_VALUE,
    )
    scheduled_at = DateTimeField()
    team_one_score = PositiveIntegerField(
        default=SCORE_DEFAULT_VALUE,
    )
    team_two_score = PositiveIntegerField(
        default=SCORE_DEFAULT_VALUE,
    )
    winner = ForeignKey(
        to=Team,
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name="won_matches",
    )

    class Meta:
        """Meta data of the table."""

        verbose_name_plural = "Matches"

    def __str__(self) -> str:
        return f"{self.team_one} vs {self.team_two}"
