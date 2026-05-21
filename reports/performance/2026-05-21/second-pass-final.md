# Second-pass performance final - 2026-05-21

## Scope

Targeted static-site-safe second pass for mobile performance and Best Practices after the first audit pass. The pass preserved the existing design system, Google Analytics, jQuery, Bootstrap, Slick, gallery, mobile navigation, bibliography behavior, contact links, and SEO/discoverability changes.

## Changes made

- Replaced the old Google WebFont JavaScript loader with HTTPS Google Fonts CSS using `font-display=optional` and non-render-blocking loading.
- Deferred non-critical icon, Magnific Popup, and Animate CSS with `media="print"` plus `noscript` fallbacks.
- Added 2x logo image candidates and wired logo `srcset`.
- Removed remaining active mixed-content-capable asset URLs from loaded CSS/JS paths.
- Converted the initial homepage hero from a CSS background to a real responsive `<picture>/<img>` LCP candidate with preload, `imagesrcset`, `fetchpriority="high"`, and mobile WebP variants.
- Kept the desktop full-width hero Slick slider, but rendered the mobile hero as a static first slide to avoid Slick wrapping the LCP element on small viewports.
- Kept the homepage mobile hero headline inside the viewport at 320 px and 390 px.
- Removed unused slider/lightbox/animation CSS from `fernando.html` and kept only the needed deferred Font Awesome stylesheet.

## Lighthouse comparison

| Route | Device | Stage | Performance | Accessibility | Best Practices | SEO | FCP | LCP | Speed Index | TBT | CLS |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `/` | Mobile | Baseline | 57 | 70 | 54 | 100 | 7.1 s | 42.2 s | 8.3 s | 0 ms | 0.002 |
| `/` | Mobile | First pass | 77 | 100 | 79 | 100 | 2.7 s | 5.1 s | 2.7 s | 0 ms | 0.002 |
| `/` | Mobile | Second pass | 80 | 100 | 100 | 100 | 1.7 s | 5.3 s | 1.7 s | 0 ms | 0 |
| `/` | Desktop | Baseline | 68 | 70 | 56 | 100 | 1.2 s | 7.1 s | 2.1 s | 0 ms | 0 |
| `/` | Desktop | First pass | 97 | 100 | 81 | 100 | 0.6 s | 1.2 s | 0.6 s | 0 ms | 0 |
| `/` | Desktop | Second pass | 97 | 100 | 100 | 100 | 0.4 s | 1.3 s | 0.4 s | 0 ms | 0 |
| `/fernando.html` | Mobile | Baseline | 59 | 82 | 57 | 100 | 6.5 s | 10.4 s | 6.5 s | 0 ms | 0 |
| `/fernando.html` | Mobile | First pass | 84 | 100 | 79 | 100 | 2.1 s | 4.3 s | 2.1 s | 0 ms | 0 |
| `/fernando.html` | Mobile | Second pass | 91 | 100 | 100 | 100 | 1.4 s | 3.5 s | 1.4 s | 0 ms | 0 |
| `/fernando.html` | Desktop | Baseline | 88 | 82 | 59 | 100 | 1.2 s | 1.9 s | 1.5 s | 0 ms | 0 |
| `/fernando.html` | Desktop | First pass | 99 | 100 | 81 | 100 | 0.5 s | 0.9 s | 0.5 s | 0 ms | 0 |
| `/fernando.html` | Desktop | Second pass | 100 | 100 | 100 | 100 | 0.3 s | 0.7 s | 0.7 s | 0 ms | 0 |

## Remaining blockers

- Homepage mobile Performance improved from 77 to 80, but remains below 90 because the legacy page still ships global jQuery/Bootstrap/Slick/plugin JavaScript, shared template CSS, and render-blocking core CSS.
- Local `python3 -m http.server` does not provide gzip/Brotli or production cache headers, so Lighthouse still reports text compression savings. Production hosting should reduce this.
- Google Analytics remains as requested. It is not blocking the main thread in the local Lighthouse run, but remains a third-party dependency.
- The homepage still has small image opportunities for below-the-fold PNG gallery/lightbox targets and review/client assets. These are not LCP-critical.

## Best Practices status

Second-pass local Best Practices is 100 on all audited routes/devices. The previous deductions were real mixed-content-capable Google Font loading and low-resolution logo delivery; both are fixed. Local HTTP itself did not remain a Best Practices blocker in the final run.

## SEO and AI discoverability safety

- `robots.txt` still references `https://ferariza.com/sitemap.xml`.
- `sitemap.xml` contains canonical production URLs for `/` and `/fernando.html`.
- `llms.txt` remains factual, simple, and explicitly experimental.
- Canonicals, OG/Twitter images, visible H1 checks, JSON-LD parsing, and noindex checks passed for `/` and `/fernando.html`.

## Verification

- `git diff --check` passed.
- `xmllint --noout sitemap.xml` passed.
- JSON-LD parse checks passed for `index.html` and `fernando.html`.
- Local asset reference checks passed for `src`, `href`, `srcset`, and `imagesrcset`.
- Local status checks returned 200 for `/`, `/fernando.html`, `/robots.txt`, `/sitemap.xml`, `/llms.txt`, and new hero/logo assets.
- Browser smoke checks passed for mobile hero rendering, mobile nav, bibliography/gallery popup, canonical/noindex checks, Fernando profile image, contact/profile links, overflow, and console health.
- Lighthouse reports were saved as `lighthouse-second-pass-local-*.report.json` and `.html`.
- Summary JSON was saved as `lighthouse-second-pass-local-summary.json`.

## Deploy readiness

Ready to deploy. The remaining homepage mobile Performance ceiling is tied to safe-to-preserve legacy architecture and production-server differences, not a known functional or SEO regression.

## Post-deploy checklist

- Open `https://ferariza.com/`.
- Open `https://ferariza.com/fernando.html`.
- Open `https://ferariza.com/robots.txt`.
- Open `https://ferariza.com/sitemap.xml`.
- Open `https://ferariza.com/llms.txt`.
- Rerun PageSpeed Insights mobile and desktop.
- Submit the sitemap in Google Search Console.
- Submit the sitemap in Bing Webmaster Tools.
- Inspect `/` and `/fernando.html` in Search Console.
- Monitor Core Web Vitals over 28 days.
