# GamerLair - defense notes

Short explanations of the project and answers to questions the teacher
may ask. Every student should read "Common topics", "Admin panel" and
the section of their own app.

---

## Common topics

### How is the project configured?

- `.env` keeps secrets: `GAMERLAIR_SECRET_KEY`, `GAMERLAIR_ENV_ID`,
  `GAMERLAIR_ADMIN_URL`. It is in `.gitignore`, so secrets never go to git.
  `.env.example` shows which variables are needed.
- `settings/conf.py` reads `SECRET_KEY` and `ENV_ID` with
  **python-decouple** (`config("NAME", cast=str)`).
- `settings/base.py` has settings common for every environment.
- `settings/env/local.py` (DEBUG=True, SQLite) and `settings/env/prod.py`
  (DEBUG=False, PostgreSQL) import everything from `base.py` and add their
  own values.
- `manage.py` and `wsgi.py` choose the settings module with
  `f"settings.env.{ENV_ID}"`, so one line in `.env` switches local / prod.
- Apps are split into `DJANGO_AND_THIRD_PARTY_APPS` and `PROJECT_APPS`.
- The admin url is also read from `.env` (`settings/urls.py`), so it can
  be hidden on production.
- Requirements are split: `requirements/base.txt` (needed everywhere),
  `dev.txt` (base + tools for development), `prod.txt` (base + PostgreSQL
  driver). `-r base.txt` includes another file.

### What is `AbstractBaseModel`? (`apps/abstracts/models.py`)

An abstract model (`class Meta: abstract = True`). Django does not create a
table for it; its fields are copied into every child model:
- `created_at` - `auto_now_add=True`, set once on creation;
- `updated_at` - `auto_now=True`, updated on every save;
- `deleted_at` - empty for normal objects.

### What is soft delete?

`delete()` is overridden: instead of removing the row it sets
`deleted_at = timezone.now()`. The data stays in the database. In the
admin panel the filter "Is deleted object" shows deleted / not deleted
objects, and the `deleted_at` column shows when it was deleted.
The bulk action "Delete selected" is turned off
(`site.disable_action`), because it deletes rows for real.

### What is the custom user? (`apps/users/models.py`)

`CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel)`:
- `AbstractBaseUser` gives password hashing (`set_password`,
  `check_password`) and `last_login`;
- `PermissionsMixin` gives `is_superuser`, `groups`, `user_permissions`;
- `AbstractBaseModel` gives our date fields and soft delete;
- `USERNAME_FIELD = "email"` - login by email;
- `REQUIRED_FIELDS = ["nickname"]` - asked by `createsuperuser`;
- `objects = CustomUserManager()` with `create_user` and
  `create_superuser`.

In settings: `AUTH_USER_MODEL = "users.CustomUser"`. It must be set before
the first migration.

**AbstractUser vs AbstractBaseUser:** `AbstractUser` already has username,
first_name, last_name, email. `AbstractBaseUser` has only password and
last_login, so we decide ourselves which fields exist.

### Relations used

| Relation | Example |
|---|---|
| One-to-many (`ForeignKey`) | `Listing.seller -> CustomUser`, `Match.tournament -> Tournament` |
| Many-to-many as a separate table with two FKs | `TeamMembership` (user + team + `is_captain`), `TournamentRegistration` (tournament + team + `is_approved`) |
| Several FKs to one model | `Match.team_one / team_two / winner -> Team`, `Review.author / target -> CustomUser`, so `related_name` is required |

### `on_delete` options

- `PROTECT` - the parent can not be deleted while children exist (used
  almost everywhere);
- `CASCADE` - children are deleted with the parent (`GameRank`: ranks
  are useless without the user).

### `related_name`

The name of the reverse relation: `user.listings.all()`,
`user.karma_votes.all()`, `tournament.matches.all()`. Without it Django
uses `<model>_set` (for example `team.teammembership_set`).

### `UniqueConstraint`

Database rule "this pair must be unique": a user can be in a team only
once, a team can register for a tournament only once, a user can review
another user only once, etc. (list in ER_DIAGRAM.md).

### `DecimalField` vs `FloatField`

Money (`price`, `prize_pool`) uses `DecimalField`: exact values, no
rounding errors like `0.1 + 0.2 = 0.30000000000000004`.

### Migrations

- `python manage.py makemigrations` - creates migration files from models;
- `python manage.py migrate` - applies them to the database.

### Management commands

- `seed_demo` (`apps/abstracts/management/commands/`) - demo data for all
  apps.
- A command is a class `Command(BaseCommand)` with method `handle()`.

### PEP8 and type annotations

- Checked with `pycodestyle --exclude=venv,migrations .` (0 errors).
- Methods have argument and return types: `def __str__(self) -> str`.
- Constants are annotated: `NAME_MAX_LEN: int = 70`.
- Admin options are annotated: `list_display: tuple[str, ...] = (...)`.
- Imports are grouped: Python modules, Django modules, Project modules.

---

## Admin panel (everyone)

Base class `AbstractBaseAdmin` (`apps/abstracts/admin.py`) is inherited by
every admin class, so common things (read-only dates, `list_per_page`)
are written once.

| Option | Meaning |
|---|---|
| `@register(Model)` | shows the model in the admin panel |
| `list_display` | columns in the list |
| `list_filter` | filters on the right side |
| `search_fields` | fields used by the search box (`user__nickname` searches through a relation) |
| `list_editable` | edit values right in the list |
| `readonly_fields` | shown but can not be changed |
| `fieldsets` | groups of fields on the edit page (only in `CustomUserAdmin`, other forms are built by Django) |
| `filter_horizontal` | two-list widget for many-to-many |
| `list_per_page` | rows per page |
| method + `short_description` | custom column (karma, score, members count) |
| `get_readonly_fields` | different read-only fields for add and change pages |
| `IsDeletedListFilter` | own filter: class `SimpleListFilter` with `lookups()` and `queryset()` |

---

## App: `users` (Student 1)

- **CustomUser** - gamer profile: email (login), nickname, Discord ID,
  Steam ID, Steam trade link, avatar url, bio, `karma` property.
- **GameRank** - rank in a game (CS2 - Global Elite). Unique pair
  (user, game_name). `on_delete=CASCADE`.
- **forms.py** - `CustomUserCreationForm` (password1 + password2, the
  password is hashed) and `CustomUserChangeForm`.
- **admin.py** - inherits `UserAdmin` to get the "add user" form and the
  "change password" page; karma column; email is read only after
  creation; admin can not delete himself.
- **Karma** = positive votes - negative votes (not deleted votes only).

Possible questions:
- *Why is the password not stored as text?* `set_password()` stores a hash
  (`pbkdf2_sha256$...`). Even an admin can not read it.
- *What does `normalize_email` do?* Makes the domain part lower case.

## App: `tournaments` (Student 2)

- **Tournament** - name, game, organizer, start date, prize pool,
  max teams, finished flag.
- **TournamentRegistration** - team registered for a tournament
  (`is_approved`). Unique (tournament, team).
- **Match** - tournament, round number, two teams, time, scores, winner.
  Three FKs to `Team`, so each has its own `related_name`; `winner` is
  `null=True` because the match may not be played yet.
- Admin: "Teams 2 / 8" column, "Score 16 : 12" column, editable
  `is_finished` and `is_approved`.

## App: `marketplace` (Student 3)

- **Game** - category of games (CS2, Dota 2...). Used by marketplace,
  teams and tournaments.
- **Listing** - offer from a seller: item or account (`is_account`),
  sale or trade (`is_trade`), price.
- **DealStatus** - statuses (Pending, Paid, Completed,
  Cancelled). A separate table, so admins can add statuses without
  changing code (same idea as `Status` in crm-django).
- **Deal** - buyer + listing + status + final price. Unique pair
  (listing, buyer).
- Admin: "Listings" count for games, editable price / status in lists.

## App: `teams` (Student 4)

- **Team** - clan: name, tag, game, owner.
- **TeamMembership** - gamer in a team (`is_captain`) - same idea as
  `UserProject` in crm-django.
- **JoinRequest** - request to join a team with a message.
- **LFGPost** - "Looking For Group": search for teammates for a game and
  rank.
- Admin: "Members" count column, editable `is_captain`, `is_accepted`,
  `is_active`.

## App: `reviews_ratings` (Student 5)

- **Review** - author, target, rating, text.
  Unique (author, target).
- **Report** - complaint: reporter, reported user, reason, resolved flag.
- **KarmaVote** - +1 / -1 (`is_positive`) from one gamer to another.
  Unique (voter, target). Karma is shown in the gamers list.
- Admin: `is_positive` column for votes, editable `is_resolved`.
