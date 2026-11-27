# Vercel deployment audit — Mac cloud app

Date: 2026-11-05. Target source branch: `noix-delf-b2-mac`.

## Verified cloud state

- Supabase organization selected by the user: `eoqgvjaduywddlkkhcsv`.
- Created project: `noix-delf-b2`, ref `dxjqnimxdcrzndpowbkl`, Singapore, ACTIVE_HEALTHY. Public schema inspected: no app tables. Security advisors returned no lints on the empty project. No application migrations or production users have been created.
- Vercel target: team `hutao` / `hutao7`, ID `team_0u84sk7bTgAXpG3S7OGGWbRY`. User membership confirmed OWNER. Project listing returned empty.
- Project creation via authenticated Vercel integration returned HTTP 403 for both configured and minimal requests. This is a provider API rejection, not proof of disconnected accounts or a reason to request tokens in chat.
- CLI fallback 65.11.0 installed; whoami reported loggedIn=false. Official login attempt failed with fetch failed, before an authorization link was issued. No deployment URL exists.

## Findings

### P0 — Private question bank would become public under a static Vite deployment

`public/content.json`, `public/audio` and `public/pdfs` are copied by Vite to public output. The current Node server protects these paths; Vercel's static asset serving would not execute that Node guard. Do not deploy current dist through a static-only project. Move licensed assets into private storage with authorization and short-lived signed URLs, and build only public UI assets into the CDN output.

### P0 — SQLite and Node process-local session storage are not the cloud persistence layer

`server/app.mjs` opens a local file database and runs process-local rate counters and cleanup timers. These are insufficient across Vercel instances/restarts. Use Supabase Auth and Postgres for real users, entitlements, atomic code redemption and revision-based progress writes. Keep RLS on every exposed table; never place service-role credentials in frontend or desktop packages.

### P1 — Protected content exceeds a Function response limit

The question bank JSON is about 11 MiB, over the documented 4.5 MB Vercel Function response-body limit. Serving it through a function as one JSON response is unsuitable. Use authenticated redirects to private object storage or smaller protected chunks. Streaming audio and PDFs should likewise use storage delivery rather than full-body function buffering.

### P1 — No cloud Auth configuration, verified mail delivery or env binding yet

Original `.env.example` describes a standalone server and Resend configuration, not a Supabase deployment. Select a Vercel project, bind real Supabase public configuration, configure real Auth redirect URLs and email delivery, then verify actual registration and reset flows. Do not bypass verification or use a simulated inbox for production.

### P1 — Initial Supabase migration is preparation, not a validated production migration

`supabase/migrations/202611050001_noix_accounts.sql` has not been applied. Review schema grants, private helpers, SECURITY DEFINER exposure, input validation and atomic concurrency behavior with current Supabase guidance before applying. Generate final migration files through the supported CLI flow and run advisors and adversarial cross-account tests after applying.

### P1 — Mac packaging is not yet an installable signed release

`desktop/main.cjs` requires a real HTTPS deployment URL. No app-config.json, Apple signing credentials, notarization result, GitHub macOS build or installer artifact exists. The workflow deliberately requires signing config; preparation files must not be presented as a finished DMG.

### P2 — Scope and release verification

Inspect the exact Vercel project/team and production/preview target before writing env vars or deploying. Do not mix the old static, standalone-server, and Mac branches. Before release, verify anonymous denial, two-account isolation, code replay, two-device sync, foreground notices, controlled updates, protected audio/PDF access and signed Mac startup.

## Next external action

Resolve the Vercel integration's create-project permission, or create an appropriate project through the user's Vercel dashboard and provide its project URL. Do not import and publish this branch as an unguarded static site. Once an authorized project can be linked, continue provisioning and environment verification before database migration/deployment.

Supabase project dashboard: https://supabase.com/dashboard/project/dxjqnimxdcrzndpowbkl

No service credentials or passwords are included here.
