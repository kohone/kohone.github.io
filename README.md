# Kohone — independent apps

Static product showcase for kohone.net, deployed through GitHub Pages.

## Build and preview

```sh
python3.14 build.py
python3 serve.py 8876
```

Open http://localhost:8876. Python 3.12+ is required for the existing legal-page generator. No Node build step is needed. Generated HTML is checked into Git.

## Add an app

1. Add its record to `products.json` with `published: false` while it is private: slug, name, short name, category, theme, tag, description, headline, icon, screen, status, and store URL (or null).
2. For an internal landing page, supply facts, story_title, story, features, pricing, and privacy. A second screenshot (`detail_screen`) and a disclaimer (`note`) are optional. For a separate product website, supply `external` instead.
3. Put optimized screenshots and icons in `assets/`. Existing themes: wood, sky, rose, moss, sand, lilac.
4. Add the app's actual privacy, support, and terms content to the generator. These are product-specific; the catalog does not invent legal policies.
5. Set `published: true` only when it should appear publicly, then run the build. Unpublished apps are excluded from the homepage, hero, related links, and generated routes; the build removes their known generated HTML pages. Cards, categories, search, internal landing pages, and related-app links are derived from the catalog. Set a real `store` URL at release; until then the page displays its development status.

Only Cycle Ally and Fair Dice are public currently. Cycle Ally links directly to its separate website, which this repository does not modify. Search and filters appear automatically once the public collection has more than four apps.

The first two public entries marked `featured` appear in the homepage phone composition. The next featured external app appears as the floating icon. With two apps, the external product supplies the floating icon. A single featured app is also supported.

## Structure

- `products.json`: product content and catalog metadata.
- `studio.py`: shared shell, homepage, and product landing templates.
- `build.py`: build entry point and established product-specific legal, support, and Fair Dice verification pages. Includes the Bowling, MGRS, and Solunar page generators from their product branches.
- `assets/site.css`: responsive visual system.
- `assets/site.js`: progressive-enhancement search and category filtering. All app links remain available without JavaScript.

Cycle Ally retains its independent website. Screenshots are development previews. Publishing is separate from local generation.

Fair Dice uses its full original body in `build.py`, styled by `.fair-landing`, rather than the generic product template. Preserve its product sections, verification links, pricing details, and FAQ when redesigning.
