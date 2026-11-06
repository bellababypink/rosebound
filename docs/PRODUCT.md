# Rosebound — product direction and delivery plan

Working name, subject to trademark and domain checks. Prepared November 5, 2026.

## Fable benchmark: evidence and limits

**Current research is blocked.** The configured egress proxy returned HTTP 403 for `https://fable.co`. No authenticated app, live screenshots, official help articles, or current store listings were inspected. This document is a provisional product analysis, not a verified audit of Fable’s latest release. Do not cite the following feature hypotheses as current Fable facts. Requested domains were saved in the environment configuration draft; that does not activate access.

Sources to inspect once access is enabled: [official website](https://fable.co), [Apple listing search](https://apps.apple.com/us/search?term=fable), [Google Play listing](https://play.google.com/store/apps/details?id=co.fable.fable), and official help links reached from the site. Verify publisher identity, release date, locale, subscription differences, and current screenshots. Help domain `help.fable.co` is a candidate, not a verified source.

| Area | Evidence status today | UX question and adaptation |
|---|---|---|
| Onboarding, personalized profiles | Unverified; requested benchmark category | Ask only high-signal preferences initially. Let readers skip or revise them. Do not infer sensitive attributes. |
| Home, navigation, social feed | Unverified | Preserve a quick path to the current book. Separate personal tasks from community activity. Verify whether the feed actually supports photos and recommendations. |
| Search and recommendations | Unverified | Title/author search, edition clarity, one-tap shelving, and transparent reasons for recommendations. |
| Lists, progress, goals, streaks, statistics | Unverified | Distinguish reading intentions from pressure. DNF is a valid state. Count distinct reading periods and rereads explicitly. |
| Ratings, reviews, wraps | Unverified | Verify rating increments and wrap export availability. Support half-stars and separate spoiler-tagged text from general reactions. |
| Clubs, private membership, organizers | Unverified | Evaluate invite expiry, roles, removal, and private-club discoverability. Give organizers a single activity and moderation view. |
| Chapter discussions | Unverified | Test whether titles, excerpts, notifications, search, and quoted replies leak spoilers. Progress gating must happen on the server. |
| Buddy reads, milestones | Unverified | Verify actual scheduling and progress-sharing affordances. Make pace-sharing optional. |
| Friends, messages, interactions | Unverified | Do not assume direct messaging exists. Build consent, blocking, reporting, and abuse response before opening messages. |
| Imports and integrations | Unverified | Verify official Goodreads import documentation and supported fields. Do not imply Kindle/Libby access. |
| TV clubs and watch tracking | Unverified | Keep later expansion separate from the primary book workflow; verify current Fable support before comparing. |
| Ebook reading and annotations | Unverified | Verify availability, content territories, purchase model, and annotation export. Metadata access never establishes ebook rights. |
| Animation, typography, layout | Screenshots not inspected | No claims about current Fable colours, motion, accessibility, or visual flaws. Evaluate hierarchy, touch targets, contrast, and reduced motion when accessible. |

The strongest **conceptual** lesson from the requested benchmark is the loop between choosing a story, recording progress, and sharing a response with other readers. That loop can make tracking feel meaningful and give clubs something concrete to discuss. Whether Fable executes each aspect exceptionally well needs direct evidence. Potential improvements below are Rosebound design opportunities, not diagnosed Fable defects.

## Adopt, improve, add

| Adopt as a category | Improve in our execution | Add to differentiate |
|---|---|---|
| Shelves, search, reading profiles | Edition-specific progress, graceful DNF, clear private/public controls | A customizable illustrated reading sanctuary |
| Progress, goals, reviews | Quiet goals, optional reminders, accessible half-star controls | Thoughtful journals and personal reading wraps |
| Clubs and discussions | Server-side spoiler gates, organizer tools, clear schedules | Clubhouse palettes, banners, reading polls |
| Reader discovery | Explainable recommendations, consent before messaging | Mood and trope preferences, optional romance controls |
| Community activity | Accessible layouts and abuse reporting before growth | Creative galleries with attribution and rights controls |
| Imports | Preview and deduplicate before committing | Exportable reading data and reversible imports |

## Original brand and design system

**Rosebound:** a little world for your reading life. Voice: warm, quietly literary, inviting to every gender and genre. Encourage curiosity rather than streak anxiety. Avoid fabricated popularity, reviews, or member counts.

Cream paper `#FCF9F3`, burgundy `#7D364C`, blush `#F1E2DF`, sage `#71806A`, chocolate ink `#463A36`, and muted gold accents. A sage theme is an equal alternative. Use Georgia for editorial headings and system sans for controls; no remote font dependency. Original typographic book illustrations clearly identified as illustrations, not publisher covers. Shelf and botanical motifs decorate without obscuring content.

Use calm transitions, visible focus, labelled inputs, native dialogs with keyboard focus containment, semantic headings, text error states, responsive grids, and reduced-motion support. Validate contrast and screen-reader flows before public launch; current automation is not a complete accessibility audit. Target at least 44px hit areas as remaining UI hardening.

## Prioritized roadmap and gates

**Phase 1 / P0 — foundation**

Delivered: signup/signin/signout, salted scrypt password storage, persistent database sessions, owner-scoped library, preference quiz, five responsive screens, genre-sorted starter recommendations, reading/finished/want/DNF/favourites shelves, editable edition page totals, progress, half-star ratings, private reviews, profile themes, goal visualization. Open Library live-search adapter exists but external lookup is blocked and unverified. Counts are actual private-library totals; no invented activity history.

Before declaring Phase 1 complete: enable and test live metadata; extend quiz with optional tropes/interests and romance preferences; custom shelves; name editing; dated reading sessions, yearly history and honest streaks; recovery and email verification; account export/deletion; deployable production server with HTTPS, durable backups, restore tests and observability. Verify these before opening social features. The present annual intention displays finished-shelf total and explicitly discloses that limitation.

**Phase 2 / P1 — social reading**

Follow/unfollow, private/public profile permissions, feed posting and deletion, friend consent, public/private clubs, expiring invitations, owner/moderator/member roles, club books and schedules, spoiler-safe chapter threads, book nominations and voting. Group chat only after block/report flows, moderator queue, rate limits, retention rules, and response policy. Spoiler gates apply to API payloads, notifications, search, quotes and attachments. Test boundary chapters and unauthorized membership. Gate: Phase 1 regression suite plus role and privacy matrix pass.

**Phase 3 / P2 — creative world**

Private journals first; quotes, notes and reactions with export. Clubhouse themes and banners. Galleries with ownership attestations, attribution, uploads scanned for abuse, reporting and takedown. Optional badges and decorations without punitive streak loss. Monthly/yearly wraps from timestamped records, preview and consent before sharing. Recommendations with editable inputs and clear explanations; no inferred intimacy preferences. Gate: moderation and content/storage cost controls validated.

**Phase 4 / P3 — events and advanced experiences**

Public reading venues and organizer events with approximate location by default, attendee privacy, capacity/waitlists, timezones, cancellation rules and reporting. Free events before payments. Ticketing requires a payment provider, organizer onboarding, refunds, tax/fee disclosure and webhook reconciliation. Goodreads CSV import with preview, field mapping, duplicates, row errors, rollback and CSV injection protections; external authorized reading links. TV/watch tracking later. Video/audio rooms require a vendor, consent, captions, controls and abuse handling. No licensed ebook library or commercial reader promised.

## Reader and organizer journeys

1. **New reader:** browse without an account → choose a story → create account → choose genres → choose mood/social pace → set optional intention/theme → home. Signup and preference saving are separate so account creation survives a dismissed quiz.
2. **Add/import:** search title/author → confirm edition → choose shelf → save → library. Later: upload CSV → preview matched/unmatched records → resolve duplicates → confirm → import summary with undo.
3. **Join club (planned):** discover by genre, pace and access → inspect rules/current book → join public club or request private membership → choose progress visibility → enter allowed chapter discussions.
4. **Organizer (planned):** create club → set privacy, rules, palette and roles → add book and schedule → invite → welcome members → moderate discussions. Owners can transfer ownership before leaving.
5. **Spoiler-safe discussion (planned):** declare progress → view only allowed threads → compose with chapter and spoiler flag → preview visibility → publish. Advancing progress requires explicit action; never reveal a future chapter in notifications.
6. **Vote (planned):** organizer opens nomination window → members nominate valid editions → eligible members vote once → results close → organizer confirms schedule. Define tie and removal behavior upfront.
7. **Review (working/private):** open saved book → half-star rating → write review → save → reopen and edit. Public sharing and spoiler visibility are later additions.
8. **Event (planned):** choose city or manually search → inspect accessibility, location, date/timezone and organizer → RSVP → private confirmation → cancel or report. No precise location collected by default.
9. **Customize (partial):** profile → edit preferences → palette, biography, intention → save → same identity across home/library. Names, custom shelf designs and favourite-book pinning follow.

## Initial five screens

| Screen | Primary action | Structure and states |
|---|---|---|
| Onboarding | Save reader preferences | Account form; three concise quiz steps; back/close controls; errors retain form input; login alternative |
| Home | Resume reading or discover a book | Editorial hero, mood shortcuts, real current reads, personalized starter collection, honest planned-community notice; no fake social feed |
| Discovery | Find and shelve a story | Title/author search, genre filters, metadata cards, shelf modal; network error, no matches, busy/disabled submit states |
| Library | Update a book | Status filters with real counts, persistent collection, edition-aware progress/rating/review dialog; signed-out and empty-shelf states |
| Profile | Personalize and see progress | Name, biography, genres, theme, library statistics, goal, favourites, signout; signed-out invitation |

## Architecture and security boundaries

Current standalone vertical slice: semantic HTML/CSS/JavaScript client, Python HTTP API, SQLite with parameterized queries and per-user row scoping. No third-party runtime dependencies. Server-generated random session tokens are stored hashed in SQLite, passwords use salted scrypt, cookies are HttpOnly/SameSite, mutation requests require JSON and same-origin checks, authentication attempts are rate-limited, and static content has a restrictive CSP. No external images or executable markup from metadata.

This is a working development build, not a production service. Python's development HTTP server must be replaced before deployment. Add TLS with secure cookies, verified proxy/host handling, email verification/recovery, privacy controls and deletion/export, durable encrypted backup/restore, request limits/timeouts, monitoring, automated migrations, security review and a proper accessibility audit. SQLite is appropriate for this small local slice; migrate through explicit schema versions to PostgreSQL for multi-instance operation, with equivalent ownership constraints and regression tests. Live search needs proxy access. No ebook rights or third-party private integration credentials are assumed.
