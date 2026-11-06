# Render hosting handoff

The environment has restored successfully. The app is present in `/workspace/rosebound`.

## Prepared and tested

- `wsgi.py`: Waitress production entrypoint; the development HTTP server is not used.
- `requirements.txt`: pinned Waitress 3.0.2.
- `render.yaml`: a single Python web service, Starter plan, a 1GB persistent disk, HTTPS-only cookies and `/api/health` readiness checks. This configuration incurs Render service and disk charges; review current pricing in Render before creating resources.
- `test_production.py`: all five API/hosting tests passed on November 6, 2026. Authentication, private library CRUD, saved progress, reviews, input/origin validation, hashed passwords, health endpoint, HEAD responses and security headers were exercised through Waitress.
- New public deployment starts with a clean database. Local synthetic/test accounts and local private reading data must never be uploaded as source.

## Remaining external prerequisites

1. Dedicated GitHub repository for this separate product. An empty private `rosebound` repository is suitable. Provide its URL; the agent must test actual Git access before pushing. Do not upload `.data`, `.runtime`, `__pycache__`, or credential files.
2. Render account connection: add `RENDER_API_KEY` securely in environment settings. A proxy-bound credential requirement targeting `api.render.com` was saved. Do not paste a key in chat. Saving this requirement does not supply a credential or deploy anything.
3. Authorize Render's GitHub integration for the private source repository. A Render API key alone does not grant private GitHub access.

Once access is available: upload source to the dedicated repository, connect it to Render, create the service from `render.yaml`, verify the build and disk mount, and test the resulting HTTPS URL. Verify live search, signup/signin, saving progress, separate-account isolation, and persistence across a service restart. Report the real URL only after it responds correctly.

No hosting account or resources were created, no purchase was made, and no public URL exists yet.

## Commands

Build: `pip install -r requirements.txt`

Start: `python wsgi.py`

Required Render settings: `ROSEBOUND_DATA=/var/data/rosebound`, `ROSEBOUND_SECURE_COOKIE=1`, disk mounted at `/var/data`. `PORT` is supplied by Render. Keep a single instance because SQLite resides on one local persistent disk. Back up SQLite using SQLite's backup API, test restores, and never treat source deployment as a database backup.

The first private release still has no password reset or email verification. Read `docs/PRODUCT.md` for remaining product/security work before inviting a broad public audience. The environment's published snapshot and a public Render deployment are separate things.
