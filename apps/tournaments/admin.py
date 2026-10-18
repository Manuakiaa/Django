# Django modules
from django.contrib.admin import register

# Project modules
from apps.abstracts.admin import AbstractBaseAdmin
from apps.abstracts.filters import IsDeletedListFilter
from apps.tournaments.models import Tournament, TournamentRegistration, Match


@register(Tournament)
class TournamentAdmin(AbstractBaseAdmin):
    """Tournament model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "name",
        "game",
        "organizer",
        "start_date",
        "prize_pool",
        "teams_count",
        "is_finished",
        "deleted_at",
    )
    list_filter: tuple = (
        "game",
        "is_finished",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "name",
        "organizer__nickname",
    )
    list_editable: tuple[str, ...] = (
        "is_finished",
    )

    def teams_count(self, instance: Tournament) -> str:
        """Registered teams / maximum teams, e.g. 2 / 8."""
        count: int = instance.tournamentregistration_set.filter(
            deleted_at__isnull=True
        ).count()
        return f"{count} / {instance.max_teams}"
    teams_count.short_description = "Teams"


@register(TournamentRegistration)
class TournamentRegistrationAdmin(AbstractBaseAdmin):
    """TournamentRegistration model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "tournament",
        "team",
        "is_approved",
        "deleted_at",
    )
    list_filter: tuple = (
        "tournament",
        "is_approved",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "tournament__name",
        "team__name",
    )
    list_editable: tuple[str, ...] = (
        "is_approved",
    )


@register(Match)
class MatchAdmin(AbstractBaseAdmin):
    """Match model admin configuration class."""

    list_display: tuple[str, ...] = (
        "id",
        "tournament",
        "round_number",
        "team_one",
        "score",
        "team_two",
        "winner",
        "scheduled_at",
        "deleted_at",
    )
    list_filter: tuple = (
        "tournament",
        "round_number",
        IsDeletedListFilter,
    )
    search_fields: tuple[str, ...] = (
        "tournament__name",
        "team_one__name",
        "team_two__name",
    )

    def score(self, instance: Match) -> str:
        """Score of the match, e.g. 16 : 12."""
        return f"{instance.team_one_score} : {instance.team_two_score}"
    score.short_description = "Score"
