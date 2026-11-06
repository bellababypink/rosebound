# Setup evidence

November 5, 2026.

- Existing checkout: `/workspace/shelf-read-sync`, clean before setup and unchanged afterward. No Git worktree was created.
- New, independent app: `/workspace/rosebound`; no changes to the selected repository’s protected files.
- Python 3.12.14 and Node 24.22.1 are available. Rosebound needs only Python standard-library modules. Chromium and Playwright are available for browser testing.
- `npm ci` for ShelfFlix failed because package.json and package-lock.json disagree (including missing Express, Drizzle, pg, tsx, and bcrypt dependencies). Fixing the tracked lockfile is a separate coding change. Its Supabase client also imports a package absent from its declared dependencies; its server requires PostgreSQL. No database URL is injected. ShelfFlix is not validated or ready.
- Initial sandboxed outbound and listening-socket operations failed. Permitted execution outside that syscall restriction allowed local server/testing and registry access through the existing proxy. TLS verification remained enabled.
- Fable official website: proxy CONNECT returned 403. Current Fable UX research remains blocked. Open Library is not in the currently enforced custom allowlist; successful live-search results have not been verified.
- Saved domain additions: fable.co, www.fable.co, apps.apple.com, play.google.com, help.fable.co, openlibrary.org. These are draft settings, not proof of runtime access.
- Rosebound API: 3 integration tests passed, exercising signup/signin/signout, preference persistence, shelf CRUD/progress/half-star review persistence, separate-account isolation, malformed input, origin rejection, duplicate email, bad password, and password hashing.
- Browser: signup → quiz → discover → save → update → library → reload → home progress; four mobile routes; signout. Passed with no page errors or horizontal overflow at 390px. Screenshots captured for desktop/mobile. This is not a complete accessibility audit.
- Runtime service: Python development server on port 5001. Processes will need restarting in new tasks.

Configuration review/publication and a fresh-task restoration test have not occurred. The new app currently lives outside the selected Git checkout and relies on the environment filesystem snapshot until placed in a dedicated repository. Do not assume it has been pushed or published.
