# Python modules
from typing import Any

# Django modules
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.exceptions import ValidationError
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    URLField,
    TextField,
    ForeignKey,
    UniqueConstraint,
    CASCADE,
)

# Project modules
from apps.abstracts.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    """Custom User Manager to make database requests."""

    def create_user(
        self,
        email: str,
        nickname: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> "CustomUser":
        """Create a regular user."""
        if not email:
            raise ValidationError(
                message="Email field is required", code="email_empty"
            )
        if not nickname:
            raise ValidationError(
                message="Nickname is required.", code="nickname_empty"
            )

        new_user: "CustomUser" = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
        self,
        email: str,
        nickname: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> "CustomUser":
        """Create super user. Used by manage.py createsuperuser."""
        return self.create_user(
            email=email,
            nickname=nickname,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """Gamer profile. Custom user model extending AbstractBaseModel."""

    EMAIL_MAX_LENGTH: int = 150
    NICKNAME_MAX_LENGTH: int = 50
    PASSWORD_MAX_LENGTH: int = 254
    EXTERNAL_ID_MAX_LENGTH: int = 100

    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        db_index=True,
    )
    nickname = CharField(
        max_length=NICKNAME_MAX_LENGTH,
        unique=True,
    )
    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
    )
    discord_id = CharField(
        max_length=EXTERNAL_ID_MAX_LENGTH,
        blank=True,
        default="",
        verbose_name="Discord ID",
    )
    steam_id = CharField(
        max_length=EXTERNAL_ID_MAX_LENGTH,
        blank=True,
        default="",
        verbose_name="Steam ID",
    )
    steam_trade_link = URLField(
        blank=True,
        default="",
    )
    avatar_url = URLField(
        blank=True,
        default="",
    )
    bio = TextField(
        blank=True,
        default="",
    )
    # True iff the user can access the admin panel
    is_staff = BooleanField(
        default=False,
    )
    # True iff the user can log in
    is_active = BooleanField(
        default=True,
    )

    REQUIRED_FIELDS: list[str] = ["nickname"]
    USERNAME_FIELD: str = "email"
    objects = CustomUserManager()

    class Meta:
        """Meta data of the table."""

        verbose_name = "Gamer"
        verbose_name_plural = "Gamers"

    def __str__(self) -> str:
        return self.nickname

    @property
    def karma(self) -> int:
        """Karma = number of positive votes - number of negative votes."""
        positive: int = self.karma_votes.filter(
            is_positive=True,
            deleted_at__isnull=True,
        ).count()
        negative: int = self.karma_votes.filter(
            is_positive=False,
            deleted_at__isnull=True,
        ).count()
        return positive - negative


class GameRank(AbstractBaseModel):
    """Rank of a gamer in a specific game (e.g. CS2 - Global Elite)."""

    GAME_NAME_MAX_LEN: int = 70
    RANK_MAX_LEN: int = 50

    user = ForeignKey(
        to=CustomUser,
        on_delete=CASCADE,
        related_name="game_ranks",
    )
    game_name = CharField(
        max_length=GAME_NAME_MAX_LEN,
    )
    rank = CharField(
        max_length=RANK_MAX_LEN,
    )

    class Meta:
        """Meta data of the table."""

        constraints = [
            UniqueConstraint(
                fields=("user", "game_name"),
                name="unique_user_game_rank",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.game_name}: {self.rank}"
