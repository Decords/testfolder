# Decords GSC growth optimization batch 1

Date: 2026-08-29
Property: https://www.decords.com/
Search Console comparison window: 2026-07-30 to 2026-08-26

## Indexing status before growth work

- Removed two obsolete redirected HTML sitemap URLs from the GSC Wizard tracker: `/pages/html-sitemap-products` and `/pages/html-sitemap-products-2`.
- Confirmed the current `/pages/sitemap`, `/pages/product-sitemap`, `/pages/collection-sitemap` and `/pages/article-sitemap` URLs are indexed.
- Confirmed Shopify Markets configuration is intentional: `www.decords.com` is the primary domain, Germany uses `decords.de`, Estonia uses `seinakleebised.ee`, and additional languages use locale subfolders on `.com`.
- The tracker reached 55 indexed URLs out of 55 before adding the growth-monitoring set.

## Query-order correction

Mushroom shelf demand changes materially with word order. The initial low-volume verification checked `mushroom floating shelf`, while the largest opportunity uses `floating mushroom shelf`. Exact Search Console API rows with `date`, `query` and `page` dimensions confirm both values.

Confirmed mushroom query examples:

| Exact query | Clicks | Impressions | Average position |
|---|---:|---:|---:|
| floating mushroom shelf | 0 | 1,027 | 9.62 |
| mushroom floating shelf | 1 | 16 | approximately 10–11 across the main product rows |
| mushroom floating wall shelf | 0 | 752 | 10.82 |
| mushroom floating shelf art | 0 | 794 | 17.51 |
| floating shelf mushroom | 0 | 636 | 14.18 |
| mushroom floating wall shelves | 0 | 479 | 13.23 |
| mushroom shelf | 1 | 197 | 10.05 |
| mushroom wall shelf | 0 | 142 | based on exact query-page rows |

Conclusion: mushroom floating shelves are the largest confirmed on-page growth opportunity in this batch. The correction is not a change in Search Console data; it fixes an earlier comparison between different exact queries.

## Confirmed baseline opportunities

| Query | Primary landing page | Clicks | Impressions | Average position |
|---|---|---:|---:|---:|
| floating mushroom shelf | `/products/3d-printed-mushroom-shelf-floating-wall-09484` plus secondary shelf pages | 0 | 1,027 | 9.62 |
| mushroom floating shelf art | primarily `/products/3d-printed-mushroom-shelf-floating-wall-09484` | 0 | 794 | 17.51 |
| mushroom floating wall shelf | primarily `/products/3d-printed-mushroom-shelf-floating-wall-09484` | 0 | 752 | 10.82 |
| floating shelf mushroom | primarily `/products/3d-printed-mushroom-shelf-floating-wall-09484` | 0 | 636 | 14.18 |
| office wall art | `/products/inspirational-home-office-decor-wall-art-74358` | 0 | 598 | 10.97 |
| clear mailing labels | `/products/custom-clear-address-labels-personalized-return-mailing-avery-shipping-stickers-personal-self-adhesive-envelope-mail-stick-lables` | 0 | 527 | 9.51 |
| floor stickers | `/products/floor-stickers-vinyl-floor-98044` | 0 | 405 | 12.72 |
| car vinyl decals | `/products/honeycomb-hood-car-decal-sport-car-34437` | 0 | 361 | 12.43 |
| window stickers | `/collections/window-stickers-and-decals` | 0 | 363 | 15.89 |

The table uses exact query strings. The non-mushroom rows use the primary English landing page and exclude small locale or product-feed parameter variants where noted.

## Shopify changes completed

### Mushroom shelf intent separation

Updated the two main mushroom shelf products without changing their handles:

- `3D Printed Mushroom Floating Shelf | Gilled Wall Ledge`
- `3D Printed Mushroom Wall Shelf | Sculpted-Gill Ledge`

The primary 09484 product now directly targets the high-volume `floating mushroom shelf` and `mushroom floating wall shelf` intent. The secondary 05272 product is differentiated as a sculpted-gill design rather than competing with identical metadata. Both products now have distinct titles, SEO metadata, introductory copy and design-specific descriptions. Both link to `/collections/3d-printed-mushroom-wall-shelves`.

### Clear mailing labels

Updated `/products/custom-clear-address-labels-personalized-return-mailing-avery-shipping-stickers-personal-self-adhesive-envelope-mail-stick-lables`:

- New product title: `Custom Clear Mailing Labels | Personalized Return Address Labels`.
- New SEO title and description focused on `clear mailing labels`.
- Added a structured comparison of Clear Gloss and White Matte.
- Added all available quantities from 45 to 450 labels.
- Added personalization, application and surface guidance.
- Clarified that these are address labels rather than postage or carrier tracking labels.

### Office wall art

Updated `/products/inspirational-home-office-decor-wall-art-74358`:

- New product title: `Inspirational Office Wall Art Decal | Motivational Success Quote`.
- New SEO title and description.
- Added exact size range, surface guidance, installation steps and FAQ.
- Added a direct internal link to `/collections/office`.

### Office values wall decals

Updated `/products/our-value-wall-decal-office-decor-sticker`:

- New product title: `Office Values Wall Decal | Motivational Workplace Word Art`.
- New SEO title and description.
- Removed the external Etsy link and unsupported universal promises.
- Replaced promotional copy with factual size, material-format, surface, installation and removal guidance.
- Added a direct internal link to `/collections/office`.

Added two other relevant office-values designs to the Office collection without merging or deleting them:

- `/products/our-values-office-wall-decal-01197`
- `/products/our-value-wall-decal-office-decor-04232`

The designs were kept separate because their artwork and value-word layouts differ.

### Floor decals

Updated `/products/floor-stickers-vinyl-floor-98044` with a direct contextual link to `/collections/3d-floor-decals-vinyl-floor-stickers`, clearly identifying the product as the dolphin design and the collection as the broader floor-decal destination.

### Car vinyl decals

Updated `/products/honeycomb-hood-car-decal-sport-car-34437`:

- Replaced generic promotional copy with factual product, size, surface and installation guidance.
- Clarified that it is a honeycomb accent graphic rather than a complete hood wrap or custom logo package.
- Added links to `/collections/car-vinyl-decals` and `/collections/car-stickers-truck-decals-vehicle-bumper-stickers`.

### 3D printed collection routing

Added a direct link from the 654-product `/collections/unique-3d-printed-home-decor-products-gifts` collection to `/collections/3d-printed-mushroom-wall-shelves`.

## Post-change indexing monitor

Added and immediately inspected 12 priority URLs, including the edited products and their target collections.

Current GSC Wizard tracker status:

- Total tracked URLs: 67
- Indexed: 67
- Not indexed: 0
- Pending: 0
- Errors: 0
- Warnings: 0

All Shopify mutations in this batch completed with zero `userErrors`.

## Measurement plan

Compare exact Search Console query-page rows after Google recrawls the updated pages. Primary metrics are clicks, impressions, CTR, average position and the distribution of mushroom shelf impressions between the primary 09484 product, the differentiated 05272 product and the dedicated mushroom shelf collection.