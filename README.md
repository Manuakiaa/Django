# GamerLair

A platform for gamers: finding teammates, organizing tournaments,
trading in-game items and reviewing other players.

The project follows the structure of
[crm-django](https://github.com/MaratulyTemirbolat/crm-django):
split settings, secrets in `.env` (python-decouple), a custom user,
an `abstracts` app with soft delete and a configured admin panel.

## Applications (5 + abstracts)

| App               | What it does                                                        | Models                                     | Responsible |
|-------------------|---------------------------------------------------------------------|--------------------------------------------|-------------|
| `users`           | Custom user (gamer profile): Discord/Steam ID, trade link, avatar, bio, game ranks, karma | CustomUser, GameRank   | Student 1   |
| `tournaments`     | Tournaments, team registration, match schedule and results          | Tournament, TournamentRegistration, Match  | Student 2   |
| `marketplace`     | Game categories, listings (items / accounts), deals and deal statuses | Game, Listing, DealStatus, Deal          | Student 3   |
| `teams`           | Clans, membership, join requests, LFG (looking for group) posts     | Team, TeamMembership, JoinRequest, LFGPost | Student 4   |
| `reviews_ratings` | Reviews, reports, profile karma                                     | Review, Report, KarmaVote                  | Student 5   |
| `abstracts`       | Shared code (not counted): base model, admin filter, base admin, `seed_demo` | AbstractBaseModel (abstract)      | everyone    |

## Requirements checklist

| Requirement | Where |
|---|---|
| Minimum 5 applications | `apps/users`, `apps/tournaments`, `apps/marketplace`, `apps/teams`, `apps/reviews_ratings` |
| Own custom user | `apps/users/models.py`: `CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel)` + `CustomUserManager`; `AUTH_USER_MODEL = "users.CustomUser"` |
| ER diagram | [ER_DIAGRAM.png](ER_DIAGRAM.png), source [ER_DIAGRAM.md](ER_DIAGRAM.md), [ER_DIAGRAM.html](ER_DIAGRAM.html) |
| Admin panel | `apps/*/admin.py` (see "Admin panel features") |
| PEP8 + type annotations | `pycodestyle` gives 0 errors; methods, constants and admin options are annotated |
| Project configuration | `settings/conf.py`, `settings/base.py`, `settings/env/local.py`, `settings/env/prod.py`, `.env`, `requirements/` |

## Project structure

```
manage.py                 chooses settings.env.<ENV_ID> from .env
.env / .env.example       secrets and environment id (.env is not in git)
requirements/
    base.txt              Django, python-decouple
    dev.txt               base + pycodestyle (PEP8 checker)
    prod.txt              base + psycopg (PostgreSQL driver)
settings/
    conf.py               SECRET_KEY, ENV_ID (python-decouple)
    base.py               common settings
    env/local.py          DEBUG=True, SQLite
    env/prod.py           DEBUG=False, PostgreSQL
    urls.py               admin url from .env
    wsgi.py
apps/
    abstracts/            AbstractBaseModel, IsDeletedListFilter,
                          AbstractBaseAdmin, command seed_demo
    users/                CustomUser, GameRank, forms
    marketplace/          Game, Listing, DealStatus, Deal
    teams/                Team, TeamMembership, JoinRequest, LFGPost
    tournaments/          Tournament, TournamentRegistration, Match
    reviews_ratings/      Review, Report, KarmaVote
```

## Run

Double click `run.bat`, or:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements\dev.txt
copy .env.example .env      # then set GAMERLAIR_SECRET_KEY
python manage.py migrate
python manage.py seed_demo  # demo data for all apps
python manage.py runserver
```

Admin panel: http://127.0.0.1:8000/admin/ - `admin@gamerlair.com` / `admin12345`

Other commands:

```powershell
python manage.py createsuperuser          # asks email and nickname
pycodestyle --exclude=venv,migrations .   # PEP8 check
```

## Admin panel features

- `list_display`, `list_filter`, `search_fields`
- `list_editable`, `fieldsets`, `readonly_fields`, `filter_horizontal`
- `list_per_page`, `ordering`
- own filter `IsDeletedListFilter` (deleted / not deleted)
- custom columns with `short_description`: "Karma", "Members",
  "Teams 2 / 8", "Score 16 : 12", "Listings"
- `get_readonly_fields`: email can not be changed after creation
- "Delete selected" action is turned off (it would delete for real,
  not soft delete)
- users: `UserAdmin` with creation form (password is hashed) and
  "change password" page

See [DEFENSE.md](DEFENSE.md) for explanations and possible questions.
