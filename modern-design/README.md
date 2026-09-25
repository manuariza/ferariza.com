# Source documentation

Production release: 25 September 2026. See the repository-root README for the current build/deployment process. Historical preview notes below describe the research and review stages. The site now replaces the old root website.

# Fernando Ariza — modern design preview

Local URL: http://127.0.0.1:8765/modern-design/

This is an isolated static route. Nothing in the published root website was changed. No dependencies were installed. No commit, push or deployment has been performed. The preview deliberately has `noindex,follow` until it is ready to launch.

## Content source of truth

Edit `data/inventory.json`, then run `python3 modern-design/scripts/build.py` from the repository root. The generator uses only the Python standard library. Generated HTML includes the bibliography, references and press archive so they remain readable without JavaScript. CSV files are review exports, not the source of truth.

- 15 book/thesis records, with category, role, year, publisher, ISBN where known, cover, sources and editorial notes.
- 51 raw academic catalogue records. Ten are book/thesis/coordination records that overlap the book inventory. The page separately presents the remaining 41 article, chapter and academic-review records.
- 136 verified press articles: 103 El Debate, 26 Zenda, five República de las Letras, two Nueva Revista. All dates populated, sorted globally newest first. Zenda dates use the visible publication label, avoiding a UTC metadata date shift. See `archiveCoverage` for discovery scope; publicly accessible archives cannot establish exhaustive lifetime output.
- Four review excerpts recovered from commit `77f019e:index.html`. The Veredas review now links to its original República de las Letras source in the inventory. The other original external URLs remain unconfirmed; Portolés is supported by the historical preview only.
- One excluded attribution retained with reasons.

## Editorial decisions

1. **Fuiste el rey** is published by **Tres Hermanas**, 2019, 220 pages (ISBN 9788412094312).
2. **Literatura y sociedad** is one intellectual work: thesis defended in 2004, published as a university electronic/memoria edition in 2006. These are not counted as two books.
3. **Bécquer**: first edition December 2006 in the bookseller record; library legal deposit 2007. Display 2006 and retain the disagreement.
4. **Construyendo puentes**: publisher edition date 3 January 2024 takes precedence over older author biographies saying 2023.
5. **Miguel Delibes**: publisher title/copyright pages say 2024; Dialnet records 2023. Display 2024. Fernando is co-editor/coordinator, not author of the entire volume.
6. **María Zambrano y las escritoras del 27** is excluded: the publisher's title page and complete contents credit other editors and do not list Fernando. Some bookseller attributions conflict with this primary source.
7. **Las adicciones en la literatura** is represented through Fernando's chapter in the academic references, not as a sole-authored book.
8. **Pío Baroja y Vicente Blasco Ibáñez** (2026) is supported by a bookseller catalogue and actual cover, with ISBN 9791387694494. Its relation to the 2017 Macrae edition remains unconfirmed; keep records distinct pending publisher/author confirmation.
9. No unverified award claim, invented review, invented ISBN, or artificial cover is displayed. All 15 records now use actual publication imagery; the thesis uses the university PDF title page.

Categories: Novelas; Biografías; Ensayo e investigación; Guías de lectura; Ediciones; Tesis. Academic articles, chapters, academic reviews, press criticism and reviews *of* Fernando's work are separate collections.

## Visual and interaction direction

Maëlan Le Meur informs the large sans-serif name, ruled horizontal divisions, moving display text and expandable index. Miranda informs the horizontal expanding bookshelf and overlapping review cards. The ornate Miranda fonts were not used. This is an original implementation in vanilla HTML/CSS/JS, not copied third-party site code.

Corpus references:
- `/Users/manuariza/Sites/design-corpus/refero-library/styles/maelan-le-meur--ea0d7b5a/`
- `/Users/manuariza/Sites/design-corpus/refero-library/styles/miranda--3f6e3076/`

Three routes into the work: featured novels; categorized interactive bookshelf; chronological searchable index. Mobile uses vertical book panels and fully readable review cards. Arrow keys/Home/End operate book spines; focus brings review cards forward. Direct links use `#libro-ID`, with browser history support. Filters support accent-insensitive matching. Reduced motion disables movement and smooth scrolling.

## Source evidence and images

`research/` contains publisher/catalogue snapshots, source screenshots and local browser screenshots. `data/image-sources.json` records downloaded cover provenance. All 15 works have actual publication imagery, with provenance and available native dimensions. New covers include Macrae, Literatura y mercado editorial, Valle-Inclán and Miguel Delibes. The thesis image is its original UCM title page. Several earlier thumbnails have been replaced with larger originals. Macrae (341 × 500) and the publisher’s Pensamiento image (366 × 569) remain limited by source resolution; no upscaling is used. El camino retains its source watermark.

The bookshelf contains 13 works. The two juvenile biographies remain in the 15-work index, and their old `#libro-` links open their index entries. The article archive offers search and one publication filter, with full dates at right. Six featured articles are editorial entry points covering narrative craft, criticism, author conversations and publishing history. Each includes its selection rationale; no objective “best articles” ranking is claimed.

Primary source precedence: publisher title/copyright page > university/library catalogue > bookseller > historical site copy. Unknown fields remain null. Brief descriptions are adaptations of existing repository copy or bibliographic titles, not invented plot details.

Research scripts use already available BeautifulSoup/Pillow and system curl for extraction; these are not website dependencies. `research.py` refreshes source snapshots only. `enrich-press.py` supplements missing dates from article metadata. Neither overwrites manually reconciled book records.

## Local development

From the repository root:

```sh
python3 modern-design/scripts/build.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open the local URL above. There is no bundler, framework, external font service, API key, analytics or backend. The existing GitHub Pages static publishing setup can serve this folder when publication is authorized.

## Remaining editorial polish

- Confirm remaining unknown page counts; Macrae ISBN and 176-page count were recovered from its Goodreads edition record.
- Locate original review URLs, especially the historical Portolés excerpt.
- Confirm the 2026 correspondence edition with its publisher and investigate the possible 2026 edition of El pensamiento narrativo before treating it as a separate edition.
- Have Fernando review the final category/role choices before replacing the main homepage.

## Daily updates and X

A discreet author-area link opens Fernando’s X profile. Daily article refresh, failure behavior, launch setup and the deferred Buffer integration are documented in [automation/README.md](automation/README.md). The updater is implemented; remote activation awaits the new-site launch.

## Technical SEO and AI discovery

Canonical/social metadata and inventory-derived JSON-LD are included without altering visible content. Production staging now supplies sitemap.xml, robots.txt, the updated experimental llms.txt guide, legacy biography/book redirects and a 404 page. The preview remains noindex. See [reports/search-review.md](reports/search-review.md) for Search Console findings, evidence and launch checks.
