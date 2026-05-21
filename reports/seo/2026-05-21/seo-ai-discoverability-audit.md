# SEO and AI Discoverability Audit - 2026-05-21

## Scope

Audited routes:

- `https://ferariza.com/`
- `https://ferariza.com/fernando.html`

The site is a static GitHub Pages site for Fernando Ariza, with homepage sections for bibliography, reviews, and contact plus a separate biography page.

## Crawlability and Indexability

| Check | Baseline Result |
|---|---|
| HTTPS apex | `https://ferariza.com/` returns 200 |
| HTTP to HTTPS | `http://ferariza.com/` redirects to HTTPS |
| `www` handling | `https://www.ferariza.com/` does not resolve |
| `/fernando.html` | returns 200 |
| `robots.txt` | 404 |
| `sitemap.xml` | 404 |
| Accidental noindex/nofollow | none found |
| Canonical URLs | missing |
| Internal linking | homepage links to `fernando.html`; biography links back to `index.html` |
| Client-side-only critical text | no; core text is in static HTML |
| Trailing slash behavior | `/` canonical route exists; `/fernando.html` is file-based |

## Metadata

Baseline:

- `lang="es"` is present.
- Viewport meta is present.
- Basic descriptions are present.
- Titles are duplicated and generic: both pages use `Fernando Ariza`.
- Canonical tags are missing.
- Open Graph tags are missing.
- Twitter/X card tags are missing.
- Theme color is missing.
- Favicon exists as `favicon.ico`; no app icons or manifest are present.
- No hreflang is needed because the site is Spanish-only.

## Structured Data

Baseline: no JSON-LD found.

Recommended schema:

- `Person` for Fernando Ariza, with accurate roles and profile links.
- `WebSite` for the official site.
- `WebPage` for the homepage and biography page.
- `BreadcrumbList` for the biography page.

Avoid:

- `FAQPage` unless a visible FAQ is added.
- `Article` unless article pages are actually published on this site.
- Fake reviews, fake awards, fake citations, or unverifiable authority signals.

## Content Quality

Strengths:

- Homepage has visible, crawlable Spanish content for works, reviews, biography summary, and contact.
- Biography page has visible, crawlable biography text.
- Important works and review excerpts are visible in HTML.

Issues:

- Homepage title and H1 emphasize book titles more than the person/site identity.
- Some image alt text is generic (`Testimonial`, `Client`).
- Icon-only links are not descriptive to assistive technologies.
- Contact email is written as plain text with spaces, which is crawlable but not a direct contact link.
- Social links have no text labels.
- The Twitter widget can hide or mutate content and creates runtime fragility.

## AI Search and Answer-Engine Readiness

Baseline gaps:

- No structured data to identify the official person/site relationship.
- No canonical URL declarations.
- No sitemap or robots file for crawlers and assistant retrievers.
- No concise machine-readable site map such as `llms.txt`.
- Some important facts are present but spread across legacy layout rather than summarized clearly in page metadata or schema.

Safe improvements:

- Add factual metadata and JSON-LD without hype.
- Add `robots.txt` and `sitemap.xml`.
- Add an optional `llms.txt` as a curated public URL map with an explicit note that it is experimental and not a ranking guarantee.
- Add descriptive accessible names and alt text so assistive and machine readers can understand links/images.
- Keep content people-first and avoid keyword stuffing or synthetic SEO pages.

## Priority Fixes

P0:

- Add `robots.txt` and `sitemap.xml`.
- Add canonical URLs and unique titles/descriptions.
- Add structured data for `Person`, `WebSite`, `WebPage`, and biography breadcrumbs.
- Fix missing accessible labels on links/buttons.
- Fix the homepage Twitter runtime error.

P1:

- Improve Open Graph and Twitter metadata.
- Add direct contact link markup where appropriate.
- Improve image alt text for meaningful images.
- Lazy-load non-critical images.

P2:

- Add `llms.txt` as a harmless documentation aid.
- Consider a future dedicated publications page only if it contains real, maintained, useful bibliographic content.
