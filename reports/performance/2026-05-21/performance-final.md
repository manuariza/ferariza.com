# Performance Final Report - 2026-05-21

## Scope

Audited the static production site and the local production-equivalent server for:

- `https://ferariza.com/`
- `https://ferariza.com/fernando.html`
- `http://127.0.0.1:4173/`
- `http://127.0.0.1:4173/fernando.html`

The site is a static GitHub Pages-style HTML/CSS/JS site. There is no package-managed build, lint, or test script in the repository, so verification used static checks, local HTTP serving, browser smoke tests, and Lighthouse CLI.

## Baseline Notes

Production PageSpeed Insights API requests returned HTTP 429 without an API key, so the production baseline used Lighthouse CLI against the live URLs. Local baseline and final results used Lighthouse CLI against `python3 -m http.server` on `127.0.0.1:4173`.

Baseline reports:

- `pagespeed-production-summary.json`
- `lighthouse-production-summary.json`
- `lighthouse-local-summary.json`
- `performance-baseline.md`

Final reports:

- `lighthouse-local-final-summary.json`
- `lighthouse-final-local-*.report.json`
- `lighthouse-final-local-*.report.html`

## Local Lighthouse Before/After

| Route | Device | Performance | Accessibility | Best Practices | SEO | LCP | FCP | CLS | TBT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `/` | mobile | 57 -> 77 | 70 -> 100 | 54 -> 79 | 100 -> 100 | 42.2 s -> 5.1 s | 7.1 s -> 2.7 s | 0.002 -> 0.002 | 0 ms -> 0 ms |
| `/` | desktop | 68 -> 97 | 70 -> 100 | 56 -> 81 | 100 -> 100 | 7.1 s -> 1.2 s | 1.2 s -> 0.6 s | 0 -> 0 | 0 ms -> 0 ms |
| `/fernando.html` | mobile | 59 -> 84 | 82 -> 100 | 57 -> 79 | 100 -> 100 | 10.4 s -> 4.3 s | 6.5 s -> 2.1 s | 0 -> 0 | 0 ms -> 0 ms |
| `/fernando.html` | desktop | 88 -> 99 | 82 -> 100 | 59 -> 81 | 100 -> 100 | 1.9 s -> 0.9 s | 1.2 s -> 0.5 s | 0 -> 0 | 0 ms -> 0 ms |

## Implemented Improvements

- Replaced the largest above-the-fold and book/profile images with modern WebP variants and responsive `picture`/`srcset` where appropriate.
- Removed the blocking Modernizr include and the fragile Twitter widget integration that produced runtime errors and third-party overhead.
- Removed the preloader markup so first paint and LCP are no longer intentionally delayed.
- Minified/pruned the largest CSS assets while restoring popup/slider CSS needed for interaction safety.
- Added `font-display: swap` to local icon fonts and reduced unused icon CSS.
- Added dimensions, `loading`, and `decoding` attributes to images to reduce layout and decode work.
- Added Slick accessibility cleanup for generated arrows and hidden slides, including `inert` handling.
- Fixed mobile bibliography card transforms so gallery controls remain reachable on small screens.
- Added a defensive Magnific Popup fallback for gallery links.
- Improved footer and page contrast to clear local Lighthouse accessibility audits.

## Remaining Performance Blockers

- Local Best Practices is capped by HTTP because the local verification server is not HTTPS. Production is HTTPS and should score higher for that audit.
- Mobile performance is still limited by the legacy static CSS/JS stack: multiple render-blocking CSS files, Slick/Bootstrap/jQuery, and background-image LCP discovery.
- Local Lighthouse flags text compression and cache lifetimes because `python3 -m http.server` does not serve production CDN headers. GitHub Pages should improve this after deploy.
- Google Analytics remains as an intentional third-party dependency and will continue to show some unused JavaScript.

## Verification

- Lighthouse CLI final pass for both routes, mobile and desktop.
- Browser smoke checks for mobile navigation, gallery popup, hidden-slide focus handling, horizontal overflow, and console errors.
- `git diff --check`
- `xmllint --noout sitemap.xml`
- Local status checks for `/`, `/fernando.html`, `/robots.txt`, `/sitemap.xml`, and `/llms.txt`
- JSON-LD parsing for `index.html` and `fernando.html`

## Production Follow-up

Production PageSpeed Insights and production Lighthouse should be rerun after deployment because the improved assets and metadata are not live until the site is published.
