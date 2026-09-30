# Daily article updates

Implemented 25 September 2026. Buffer publishing implementation added 30 September 2026; activation requires BUFFER_API_KEY and the X enable variable. The public site has a plain profile link; no X widgets or tracking scripts were added.

## What runs

`python3 modern-design/scripts/update-articles.py` performs a read-only dry run. Add `--write` to persist validated new records. Uses Python's standard library and system curl, without installing packages.

The updater follows all archive pagination for El Debate and Zenda, deduplicates canonical URLs, checks the article author metadata, and reads the displayed publication date (including Zenda's local date rather than its UTC metadata date). Existing descriptions, dates, editorial corrections and featured choices are never overwritten. Other publications already in the inventory remain intact.

Both sources must validate before any inventory write. Empty archives, suspicious coverage drops, invalid dates, changed authorship markup, cross-publisher canonical URLs and ID collisions fail the run. Missing old links are never deleted. A failed refresh cannot deploy a partial website. The archive is globally sorted by publication date at build time.

## Workflow and activation

The user approved full activation on 25 September 2026. The active workflow is `.github/workflows/daily-articles.yml`; the repository variable ARTICLE_UPDATES_ENABLED is true. The earlier template is retained as implementation history.

Launch configuration and maintenance checklist:

1. Commit and push the new design, scripts, tests and workflow to the default branch.
2. Set GitHub Pages source to **GitHub Actions**, retaining the configured custom domain `ferariza.com`.
3. Permit the workflow to write repository contents (or use the repository's approved automation credentials if branch protection prevents its inventory commits). The built-in GITHUB_TOKEN is otherwise sufficient; no personal access token or publisher credentials are needed.
4. Set the Actions repository variable `ARTICLE_UPDATES_ENABLED=true`.
5. Run the workflow manually once and verify the deployed root page and the Actions summary.
6. Enable GitHub Actions failure notifications for the account responsible for the scheduled workflow. Failures produce a failed run and summary; notification delivery depends on that account's GitHub settings.

The schedule runs daily at 06:23 UTC (07:23 winter / 08:23 summer in Madrid), plus manual runs and relevant pushes. It runs only on the default branch and is guarded by the enable variable. A shared concurrency group serializes runs; a competing source commit causes the non-force push to fail instead of being overwritten.

The same workflow explicitly uploads and deploys the Pages artifact; it does not rely on an automation commit triggering another build. Only index.html, CSS, JS and images are staged. Research, datasets, scripts and credentials are excluded. The source preview retains noindex, while the staged production homepage is indexable. The old /fernando.html URL redirects to /#autor.

A small `refresh-health.json` commit is made on the first successful run of each UTC month, even when no articles are new. This provides regular repository activity and a visible health record to reduce the risk of GitHub's 60-day inactive-public-repository schedule shutdown. It is not an independent uptime monitor. If the schedule stops or is disabled, re-enable it in Actions, inspect failures and run it manually; a disabled workflow cannot notify about its own inactivity. GitHub may delay scheduled runs.

Stop daily refresh/deployment by setting `ARTICLE_UPDATES_ENABLED=false` or disabling the workflow. X has its own enable switch, described below.

## Verified action release ages

Release dates were checked with GitHub's public releases API on 2026-09-25. Each action is pinned to its corresponding commit in the template:

- actions/checkout v4.2.2 — 2024-10-23.
- actions/upload-pages-artifact v3.0.1 — 2024-02-07.
- actions/deploy-pages v4.0.5 — 2024-03-18.

All exceed the seven-day requirement. No package manifests or lockfiles are changed.

## Checks completed

- Eight standard-library unit tests: source markup failure, publication dates, authorship rejection, canonical-host validation, duplicate handling, pagination, preservation of editorial content and partial archive detection.
- Live dry run: six El Debate archive pages / 103 distinct articles; four Zenda archive URLs (including its page-one alias) / 26 distinct articles. No new records found; existing 136-record inventory unchanged.
- Production staging uses only local public assets and does not include the old design.

## Automatic X publishing through Buffer

After a successful website deployment, `publish-x` posts each newly inventoried El Debate/Zenda article to `ferariza_` with `Nuevo artículo en [publication]:` and the original URL. Uses Buffer GraphQL `shareNow`, no drafts, reviews, AI generation or extra dependencies. Detection follows the daily article checks; GitHub schedule delays remain possible.

Activation: store a Buffer personal key in repository Actions secret `BUFFER_API_KEY`; set `BUFFER_CHANNEL_ID=6abcd038ea19ca0bde30b8c0` and `TWITTER_UPDATES_ENABLED=true` in repository Actions variables. Only account read, posts read and posts write permissions are needed. Keep the key's expiry monitored and replace the secret before expiration.

Disable X independently with `TWITTER_UPDATES_ENABLED=false`. Website updates continue. Articles discovered while disabled remain eligible on reactivation; already submitted articles are not repeated.

`modern-design/data/twitter-ledger.json` excludes 129 historical source articles at initial setup. Each submission records a Buffer post ID. Intent is committed and pushed before creating a post. After a timeout or interrupted run, the next run checks Buffer posts and reconciles a matching URL; if absent it stops for inspection rather than risking a duplicate. Confirmed API rejections stay retryable on later daily runs. Delivery errors on an existing post require resolution in Buffer. A successful API submission does not prove X delivery; check Buffer's Sent/Error state.

For an uncertain `attempting` entry, inspect Buffer first. If no post exists and creation definitively failed, change that entry's status to `retry` and rerun the workflow. Never delete the ledger or reset the baseline.

References:
- https://developers.buffer.com/guides/posts-and-scheduling.html
- https://developers.buffer.com/types/ShareMode.html
- https://buffer.com/api
