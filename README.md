# Fernando Ariza — ferariza.com

The current author website is published at https://ferariza.com/ using GitHub Pages.

## Editing and publishing

Editable site source is in `modern-design/`. The root HTML/CSS/images are generated copies of the current website, not the previous design. Update the inventory at `modern-design/data/inventory.json`, then run:

```sh
python3 modern-design/scripts/build.py
python3 modern-design/scripts/prepare-pages.py
python3 modern-design/scripts/sync-root.py
python3 -m unittest discover -s modern-design/scripts -p 'test_*.py'
```

Commit source and generated root changes to `master`. The Pages workflow explicitly deploys `_site/`, excluding source, research and internal documentation. Old biography/book routes redirect to the relevant new sections. Git history retains the retired design.

## Daily updates

`.github/workflows/daily-articles.yml` checks El Debate and Zenda at 06:23 UTC daily, and supports manual runs. Validated new articles are committed to the inventory and generated website, then deployed. Existing editorial selections and other publications remain intact. Failures stop deployment. Set repository variable `ARTICLE_UPDATES_ENABLED=false` to pause refresh and deployment.

The same concurrency group serializes deployments. A monthly successful-run record maintains repository activity even when no articles appear. Check the Actions page for failures and keep GitHub notification settings enabled; a disabled schedule cannot report its own inactivity.

## Deferred

Buffer/social posting is not enabled. The site links to Fernando's X profile only.

See `modern-design/automation/README.md` for implementation details and `modern-design/reports/search-review.md` for the pre-launch SEO baseline.
