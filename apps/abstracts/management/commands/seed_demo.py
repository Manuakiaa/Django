# Python modules
from datetime import timedelta
from typing import Any

# Django modules
from django.core.management.base import BaseCommand
from django.utils import timezone

# Project modules
from apps.marketplace.models import Deal, DealStatus, Game, Listing
from apps.reviews_ratings.models import KarmaVote, Report, Review
from apps.teams.models import JoinRequest, LFGPost, Team, TeamMembership
from apps.tournaments.models import Match, Tournament, TournamentRegistration
from apps.users.models import CustomUser, GameRank


class Command(BaseCommand):
    """Fill the database with demo data: python manage.py seed_demo"""

    help = "Fill the database with demo data for all apps"

    PASSWORD: str = "gamer12345"

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Command entry point."""

        if CustomUser.objects.filter(email="admin@gamerlair.com").exists():
            print("Demo data already exists.")
            return

        # ---------- users ----------
        CustomUser.objects.create_superuser(
            email="admin@gamerlair.com",
            nickname="admin",
            password="admin12345",
        )
        s1mple: CustomUser = CustomUser.objects.create_user(
            email="s1mple@gamerlair.com",
            nickname="s1mple",
            password=self.PASSWORD,
            discord_id="s1mple#0001",
            steam_id="76561198034202275",
            bio="AWP player",
        )
        zywoo: CustomUser = CustomUser.objects.create_user(
            email="zywoo@gamerlair.com",
            nickname="ZywOo",
            password=self.PASSWORD,
        )
        miracle: CustomUser = CustomUser.objects.create_user(
            email="miracle@gamerlair.com",
            nickname="Miracle",
            password=self.PASSWORD,
        )
        GameRank.objects.create(
            user=s1mple, game_name="CS2", rank="Global Elite"
        )
        GameRank.objects.create(user=zywoo, game_name="CS2", rank="Supreme")
        GameRank.objects.create(
            user=miracle, game_name="Dota 2", rank="Immortal"
        )

        # ---------- marketplace ----------
        cs2: Game = Game.objects.create(name="CS2")
        dota: Game = Game.objects.create(name="Dota 2")
        Game.objects.create(name="Valorant")

        pending: DealStatus = DealStatus.objects.create(name="Pending")
        DealStatus.objects.create(name="Paid")
        completed: DealStatus = DealStatus.objects.create(name="Completed")
        DealStatus.objects.create(name="Cancelled")

        dragon_lore: Listing = Listing.objects.create(
            seller=s1mple,
            game=cs2,
            title="AWP | Dragon Lore",
            price="1500.00",
        )
        arcana: Listing = Listing.objects.create(
            seller=miracle,
            game=dota,
            title="Arcana for Invoker",
            price="35.00",
            is_trade=True,
        )
        Deal.objects.create(
            listing=dragon_lore,
            buyer=zywoo,
            status=completed,
            final_price="1400.00",
        )
        Deal.objects.create(
            listing=arcana,
            buyer=s1mple,
            status=pending,
            final_price="35.00",
        )

        # ---------- teams ----------
        navi: Team = Team.objects.create(
            name="Natus Vincere", tag="NAVI", game=cs2, owner=s1mple
        )
        vitality: Team = Team.objects.create(
            name="Team Vitality", tag="VIT", game=cs2, owner=zywoo
        )
        TeamMembership.objects.create(user=s1mple, team=navi, is_captain=True)
        TeamMembership.objects.create(
            user=zywoo, team=vitality, is_captain=True
        )
        JoinRequest.objects.create(
            user=miracle, team=navi, message="I can play CS too!"
        )
        LFGPost.objects.create(
            author=miracle,
            game=dota,
            rank_required="Divine",
            description="Looking for 4 players for ranked.",
        )

        # ---------- tournaments ----------
        cup: Tournament = Tournament.objects.create(
            name="GamerLair CS2 Cup",
            game=cs2,
            organizer=s1mple,
            start_date=timezone.now() + timedelta(days=7),
            prize_pool="10000.00",
        )
        TournamentRegistration.objects.create(
            tournament=cup, team=navi, is_approved=True
        )
        TournamentRegistration.objects.create(tournament=cup, team=vitality)
        Match.objects.create(
            tournament=cup,
            team_one=navi,
            team_two=vitality,
            scheduled_at=timezone.now() + timedelta(days=7),
            team_one_score=16,
            team_two_score=12,
            winner=navi,
        )

        # ---------- reviews and ratings ----------
        Review.objects.create(
            author=zywoo, target=s1mple, rating=5, text="Fast deal"
        )
        Review.objects.create(
            author=s1mple, target=miracle, rating=3, text="Slow answers"
        )
        Report.objects.create(
            reporter=zywoo,
            reported_user=miracle,
            reason="Toxic behaviour in the chat",
        )
        KarmaVote.objects.create(voter=zywoo, target=s1mple, is_positive=True)
        KarmaVote.objects.create(
            voter=miracle, target=s1mple, is_positive=True
        )
        KarmaVote.objects.create(
            voter=s1mple, target=miracle, is_positive=False
        )

        print("Demo data created.")
        print("Admin: admin@gamerlair.com / admin12345")
        print(f"Gamers: s1mple, ZywOo, Miracle / {self.PASSWORD}")
