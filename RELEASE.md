# Production release — 25 September 2026

Live URL: https://ferariza.com/

Release commit: 3ad9ae6. First automatic health commit: e4644ca.
Successful refresh/deploy: https://github.com/manuariza/ferariza.com/actions/runs/36116096128

## Completed

- Replaced the old root website and removed retired design assets from the current branch; history preserves them.
- Activated GitHub Actions Pages publishing, keeping the ferariza.com custom domain and enforced HTTPS.
- Enabled ARTICLE_UPDATES_ENABLED=true and the 06:23 UTC daily schedule.
- First cloud run passed all 13 tests, fetched both complete author archives (103 El Debate / 26 Zenda), persisted its monthly health record and deployed successfully. No new articles were found.
- Production browser verified 13 shelf entries, 136 archive entries, all images loaded, canonical root and indexable metadata, mobile layout without horizontal overflow, and working publication filtering.
- Verified legacy biography, both book links and preview hashes redirect to the matching new homepage sections.
- Unknown route returns HTTP 404; HTTP root redirects to HTTPS with 301.
- Resubmitted https://ferariza.com/sitemap.xml in Search Console. Google reports Success, read/submitted September 25, 2026, with one discovered canonical page.

- Homepage indexing request accepted by Google; URL added to its priority crawl queue.

## Operations

Daily ingestion covers El Debate and Zenda. The additional verified Nueva Revista and República de las Letras archive entries remain on the site; those publishers are not daily ingestion sources. Existing editorial selections and corrected records are preserved. Buffer remains deferred.

GitHub can delay schedules; successful monthly health commits maintain repository activity. Failed refreshes leave the currently deployed site intact. The owner should retain Actions failure notifications and inspect any disabled workflow. Runtime deprecation notices were non-fatal on the successful release run; action upgrades remain subject to the repository's dependency approval rules.

The optional www.ferariza.com alias did not resolve in the launch check. The configured canonical ferariza.com domain works with valid HTTPS. Adding a www DNS alias would require DNS-provider access; it is not required for the canonical site's launch.

Search indexing and rankings update asynchronously. No immediate ranking or recrawl completion is claimed.
