# GamerLair - ER diagram

Every table also has `created_at`, `updated_at` and `deleted_at`
(inherited from `abstracts.AbstractBaseModel`). They are hidden below
to keep the diagram readable.

```mermaid
erDiagram
    CustomUser ||--o{ GameRank : "has"
    CustomUser ||--o{ Listing : "sells"
    CustomUser ||--o{ Deal : "buys"
    CustomUser ||--o{ Team : "owns"
    CustomUser ||--o{ TeamMembership : "is member"
    CustomUser ||--o{ JoinRequest : "sends"
    CustomUser ||--o{ LFGPost : "writes"
    CustomUser ||--o{ Tournament : "organizes"
    CustomUser ||--o{ Review : "writes / receives"
    CustomUser ||--o{ Report : "sends / receives"
    CustomUser ||--o{ KarmaVote : "gives / receives"

    Game ||--o{ Listing : "category of"
    Game ||--o{ Team : "played by"
    Game ||--o{ LFGPost : "for"
    Game ||--o{ Tournament : "for"

    Listing ||--o{ Deal : "has"
    DealStatus ||--o{ Deal : "status of"

    Team ||--o{ TeamMembership : "has"
    Team ||--o{ JoinRequest : "receives"
    Team ||--o{ TournamentRegistration : "registers"
    Team ||--o{ Match : "plays / wins"

    Tournament ||--o{ TournamentRegistration : "has"
    Tournament ||--o{ Match : "has"

    CustomUser {
        bigint id PK
        string email UK
        string nickname UK
        string password
        string discord_id
        string steam_id
        string steam_trade_link
        string avatar_url
        text bio
        bool is_staff
        bool is_active
        bool is_superuser
        datetime last_login
    }
    GameRank {
        bigint id PK
        bigint user_id FK
        string game_name
        string rank
    }
    Game {
        bigint id PK
        string name UK
    }
    Listing {
        bigint id PK
        bigint seller_id FK
        bigint game_id FK
        string title
        text description
        decimal price
        bool is_account
        bool is_trade
        bool is_active
    }
    DealStatus {
        bigint id PK
        string name UK
    }
    Deal {
        bigint id PK
        bigint listing_id FK
        bigint buyer_id FK
        bigint status_id FK
        decimal final_price
    }
    Team {
        bigint id PK
        string name UK
        string tag
        text description
        bigint game_id FK
        bigint owner_id FK
    }
    TeamMembership {
        bigint id PK
        bigint user_id FK
        bigint team_id FK
        bool is_captain
    }
    JoinRequest {
        bigint id PK
        bigint user_id FK
        bigint team_id FK
        text message
        bool is_accepted
    }
    LFGPost {
        bigint id PK
        bigint author_id FK
        bigint game_id FK
        string rank_required
        text description
        bool is_active
    }
    Tournament {
        bigint id PK
        string name
        text description
        bigint game_id FK
        bigint organizer_id FK
        datetime start_date
        decimal prize_pool
        int max_teams
        bool is_finished
    }
    TournamentRegistration {
        bigint id PK
        bigint tournament_id FK
        bigint team_id FK
        bool is_approved
    }
    Match {
        bigint id PK
        bigint tournament_id FK
        bigint team_one_id FK
        bigint team_two_id FK
        bigint winner_id FK
        int round_number
        datetime scheduled_at
        int team_one_score
        int team_two_score
    }
    Review {
        bigint id PK
        bigint author_id FK
        bigint target_id FK
        int rating "1..5"
        text text
    }
    Report {
        bigint id PK
        bigint reporter_id FK
        bigint reported_user_id FK
        text reason
        bool is_resolved
    }
    KarmaVote {
        bigint id PK
        bigint voter_id FK
        bigint target_id FK
        bool is_positive
    }
```

## Apps and tables

| App               | Tables                                        |
|-------------------|-----------------------------------------------|
| `users`           | CustomUser, GameRank                          |
| `marketplace`     | Game, Listing, DealStatus, Deal               |
| `teams`           | Team, TeamMembership, JoinRequest, LFGPost    |
| `tournaments`     | Tournament, TournamentRegistration, Match     |
| `reviews_ratings` | Review, Report, KarmaVote                     |

## Unique constraints

- `GameRank`: (user, game_name)
- `Deal`: (listing, buyer)
- `TeamMembership`: (user, team)
- `JoinRequest`: (user, team)
- `TournamentRegistration`: (tournament, team)
- `Review`: (author, target)
- `KarmaVote`: (voter, target)
