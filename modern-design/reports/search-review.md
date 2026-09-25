# Technical search and AI discovery review — 25 September 2026

## Scope and release identity

Domain: https://ferariza.com/; locale: Spanish. Scope: the new static landing page and its production staging pipeline. Local uncommitted work, not a deployed release. Visible design and content are unchanged: the generated body HTML was compared byte-for-byte before/after and is identical.

Blueprint reviewed:
- `_projects/ai_coding_master_blueprint/stage-2-helm/docs/growth/search-discovery-plan.md`
- `_projects/ai_coding_master_blueprint/stage-4-perfect/SEARCH-REVIEW-template.md`

The blueprint distinguishes local eligibility from production verification and eventual ranking. No new content pages, keyword stuffing, hidden prose, fabricated review ratings, AI-only versions or unverified claims were added.

## Production baseline (authenticated Search Console)

Property: sc-domain:ferariza.com. Page indexing: All known pages, last updated September 21, 2026. Two indexed URLs; six excluded URLs across four categories: redirect (2), 404 (1), alternate with proper canonical (1), crawled/currently not indexed (2). Redirect and duplicate exclusions are not inherently errors.

Sitemap https://ferariza.com/sitemap.xml: Success; submitted May 21, 2026; last read September 22, 2026; two discovered pages. Live XML still lists `/` and `/fernando.html`, which match the old site's current structure.

Homepage URL Inspection (indexed snapshot, not a live test): URL is on Google; indexed; last crawl September 18, 2026 at 7:14:58 PM as Googlebot smartphone. Crawl allowed, successful fetch, indexing allowed. Declared canonical https://ferariza.com/ and Google-selected canonical is the inspected URL. HTTPS is reported. The inspection's sitemap association shows “Temporary processing error” while the separate sitemap report shows Success; neither was presented as proof of a failed sitemap or changed to conceal the discrepancy.

Legacy URLs observed:
- `/ciudad-dormida.html`: 404 report, last crawled May 8, 2026.
- `/fuiste-el-rey.html`: crawled/not indexed report, last crawled April 24, 2026; current public fetch returns 404.
- `/cookies.html`: crawled/not indexed report, last crawled March 15, 2026; current public fetch returns 404. No equivalent new cookie page exists; leave a genuine 404 rather than redirect an unrelated policy URL to the homepage.

Live homepage returns HTTP 200 from GitHub Pages, Last-Modified May 21, 2026. The new design is still local. No Search Console resubmission, validation request or indexing request was made for local-only changes. No performance/traffic export, actual Core Web Vitals measurement, rich-result eligibility or search ranking was claimed.

## Changes implemented and locally verified

| Area | Implementation | Status |
|---|---|---|
| Canonical | One absolute https://ferariza.com/ canonical; query variants share the root target | Locally verified |
| Metadata | Preserve title/description; add Open Graph and X card metadata, real portrait, favicon | Locally verified |
| Entity information | JSON-LD Person, WebSite, WebPage, bibliography ItemList and 15 Book/CreativeWork records derived from the inventory | Locally verified |
| Attribution | Edition/coordinated volume records use contributor rather than inventing sole authorship; no review stars or offers | Locally verified |
| Rendering | Bibliography, article archive and biography remain in delivered HTML; no JavaScript fetch needed to retrieve them | Locally verified |
| Index control | Local preview remains noindex; staged production is index,follow,max-image-preview:large | Locally verified |
| Sitemap | Production XML lists only the canonical homepage; fragments/external articles/redirects are excluded; omit unreliable lastmod | Locally verified |
| Robots | Public root/assets crawlable with sitemap declaration; no new restrictions on search or AI crawlers | Locally verified |
| AI guide | Preserve experimental llms.txt navigation aid with current section URLs; explicitly not a ranking mechanism | Locally verified |
| Staging | Public HTML/CSS/JS/images/favicon/robots/sitemap only plus redirect/error files; no research or data directories | Locally verified |
| Migration | Old biography → /#autor; Ciudad dormida → /#libro-ciudad-dormida; Fuiste el rey → /#libro-fuiste-el-rey; preview route → root, retaining hashes in browsers | Locally verified |
| Unknown routes | Dedicated noindex 404.html, served with 404 by GitHub Pages; no blanket homepage redirect | Generated; HTTP status needs production verification |
| Locale | html lang=es and es_ES social locale; no hreflang because there are no translated equivalents | Locally verified |

GitHub Pages cannot configure arbitrary native 301 responses. Legacy pages use immediate meta-refresh redirects, which Google supports as permanent redirects; a future edge layer can replace these with HTTP 301s. Browser hashes identify sections, not independently indexable book landing pages. Keeping the single-page design means individual books are not separate canonical pages.

## AI discovery interpretation

The useful foundation is crawlable HTML, clear factual attribution, canonical URLs and accurate visible content. Google does not require special AI markup or llms.txt for AI Overviews/AI Mode. OpenAI documents OAI-SearchBot separately from GPTBot training controls; the current allow-all policy already permits search crawling. Actual crawler access can also depend on hosting behavior. No promise of citations, indexing or rankings is made.

## Verification and remaining launch work

Thirteen standard-library tests passed across updater and SEO checks. SEO checks cover canonical/index controls, structured records and contributor attribution, sitemap membership, local asset existence, exclusion of build internals, redirects and error-page noindex. Generated body equals the pre-change body byte-for-byte. No packages installed and no dependencies changed.

At launch (owner: site maintainer, before/after deployment):
1. Deploy the staged new root site using the agreed release process. The earlier official Actions dependency approval remains pending; this review does not silently approve dependencies or enable automation.
2. Verify root 200, www/HTTP canonicalization, sitemap/robots 200, production indexability, social image loading, old-page redirects and arbitrary missing-path 404 on the public domain.
3. Keep the same Search Console domain property; no Change of Address operation is needed for an unchanged domain.
4. Resubmit the existing sitemap URL after its new contents are live; request homepage indexing once and validate the resolved old-book 404 after live verification. Do not submit localhost, fragment URLs or the preview as separate pages.
5. Inspect Google-selected canonical and indexing once recrawled; a smaller indexed-page count is expected when biography and work URLs consolidate into the homepage.
6. Review Search Console Web performance using the same date/device/country filters over a sufficient post-launch period. Track branded author/book queries, impressions and clicks; compare against a saved baseline and note the redesign as a confounder. Check Core Web Vitals if field data exists. No universal waiting period guarantees indexing.

## Sources

- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://developers.google.com/search/docs/crawling-indexing/301-redirects
- https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- https://developers.openai.com/api/docs/bots
