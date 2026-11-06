# Rosebound

An original, separate social-reading product foundation. The existing ShelfFlix repository is unchanged.

Start with Python 3.12 or later:

```sh
cd /workspace/rosebound
python3 server.py
```

Default port: 5001. `PORT` overrides it. SQLite lives at `.data/rosebound.sqlite3`; `ROSEBOUND_DATA` can select another durable directory. Never commit database files, account data or sessions. No dependencies need installing for the app itself. The cloud onboarding UI does not support localhost preview links.

Functional: real accounts, persistent private shelves, onboarding preferences, progress, reviews, ratings, theme selection and statistics. Live search uses Open Library but requires permitted network access. Starter-book data and original illustrated covers remain available without it. Social clubs, messages, imports, events and artwork sharing are roadmap items.

Validation:

```sh
python3 test_journeys.py
node --check public/app.js
python3 test_browser.py
```

Browser validation additionally needs the environment's existing Playwright Python package and Chromium. Tests use synthetic accounts; `test_journeys.py` creates an isolated temporary database. Browser tests use the running development server and create a synthetic account there.

Read [product direction and roadmap](docs/PRODUCT.md) for the provisional benchmark analysis, six requested planning deliverables, scope and production requirements. [Setup evidence](docs/SETUP.md) records the environment limitations. This server is intended for development, not Internet deployment. Set `ROSEBOUND_SECURE_COOKIE=1` only behind HTTPS; production hosting requires the hardening described in the product plan.

## Web hosting

Render deployment configuration is prepared in `render.yaml`. Install `requirements.txt` and start `python wsgi.py` for the production server. See [hosting status and connection steps](docs/HOSTING.md). The environment has restored, but no public deployment exists until a Render account and source repository are connected.
