# Decords GSC Growth Batch 11

Date: 2026-08-30
Store: https://www.decords.com/
Search Console source period: 2026-07-31 to 2026-08-27

## Selection method

This batch began with a review of all ten previous GSC growth audit files and the live Shopify `updatedAt` values of candidate landing pages. Pages that had already been substantially edited from 2026-08-27 through 2026-08-30 were excluded from another full rewrite so their earlier changes can be evaluated after Google recrawls them.

Six collection pages were inspected in detail but deliberately left unchanged because their descriptions, SEO fields and internal structure were already current: Fantasy & Mythology, Housewarming, Bathroom, Living Room, Easter and Game Room.

Additional product candidates were also excluded after the live audit showed recent updates on 2026-08-29 or 2026-08-30. These included mailbox decals, frosted glass wave film, picture-frame stickers, makeup-brush holders, electrical identification labels, celestial ceiling decals, racing stripes, vinyl letter sets, whale nursery decals, funny dog decals and black angel wings.

The remaining safe opportunities were two older commercial pages:

1. An active neon controller product last updated on 2026-08-26, with an older Google landing URL correctly redirected to the active product.
2. A refrigerator-door vinyl product last updated on 2026-08-15, with a generic legacy description and no membership in the two most relevant kitchen collections.

## Search opportunities used

| Query | Landing page observed in GSC | Clicks | Impressions | CTR | Average position |
|---|---|---:|---:|---:|---:|
| gamer wall decals | `/products/3d-gamer-wall-decal-neon-game-11424` | 0 | 71 | 0% | 6.80 |
| gamer wall stickers | `/products/3d-gamer-wall-decal-neon-game-11424` | 0 | 38 | 0% | 13.63 |
| video game wall decals | `/products/3d-gamer-wall-decal-neon-game-11424` | 0 | 19 | 0% | 10.84 |
| game room decals | `/collections/game-room` | 1 | 63 | 1.59% | 6.05 |
| fridge vinyl | `/collections/food-beverages` | 0 | 62 | 0% | 7.69 |
| refrigerator door covers | `/collections/food-beverages` | 0 | 57 | 0% | 9.18 |

The refrigerator queries were primarily landing on the Food & Beverages collection. The product was therefore added to that manual collection and to the Kitchen collection, while the product page itself was rewritten to become a stronger dedicated landing page.

## Summary of completed changes

| Action | Count |
|---|---:|
| Product pages fully rewritten | 2 |
| Product titles updated | 2 |
| Product types clarified | 2 |
| Product SEO titles updated | 2 |
| Product SEO descriptions updated | 2 |
| Precise product tags installed | 27 |
| Manual thematic collection relationships added | 2 |
| Internal product or collection links added | 4 |
| Redirects changed | 0 |
| Products archived or deleted | 0 |
| Handles or customer-facing URLs changed | 0 |

## Product 1: neon controller gamer wall decal

Product ID: `gid://shopify/Product/10567324041554`

Previous title:

`3D Neon Game Controller Wall Decal | Brick Breakthrough`

New title:

`3D Gamer Wall Decal | Neon Controller Brick Breakthrough`

Current URL:

`https://www.decords.com/products/neon-game-controller-wall-decal`

New product type:

`Gaming Wall Decals`

New SEO title:

`3D Gamer Wall Decal | Neon Controller Brick Effect`

New SEO description:

`Flat printed 3D-effect gamer wall decal with a neon controller breaking through brick. Compare 8–118 inch sizes, wall preparation and installation.`

### Content changes

The page now states clearly that:

- the product is one flat printed vinyl decal;
- the brick opening, shadows, glow and depth are optical effects;
- the product is not a raised 3D object;
- it is not an LED sign or real neon light;
- the design does not emit light;
- the selected size is the longest side of the complete composition;
- the second dimension changes proportionally;
- available options run from 8 inches to 118 inches;
- mock-ups do not establish exact scale;
- large sizes may be produced in aligned sections;
- walls must be clean, dry, smooth, stable and fully cured;
- installation, alignment, care and removal limitations are explained.

The page includes a comparison link to the second active neon-controller design and a link to the Game Room collection. The second controller product was not edited because it had already been updated on 2026-08-28 and uses different artwork.

### Legacy redirect retained

The old Google landing path remains correctly redirected:

`/products/3d-gamer-wall-decal-neon-game-11424`

Target:

`/products/neon-game-controller-wall-decal`

Redirect ID:

`gid://shopify/UrlRedirect/1759180030290`

No redirect was added, removed or changed in this batch.

## Product 2: refrigerator door vinyl wrap

Product ID: `gid://shopify/Product/8755053101394`

Previous title:

`Fridge Door Wrap Vinyl Sticker - Skin Decor Front Refrigerator Decoration Wallpaper Decal - Covering Freezer Art Peel And Stick Mural`

New title:

`Fridge Door Wrap Vinyl Sticker | Refrigerator Door Cover`

Current URL:

`https://www.decords.com/products/fridge-door-wrap-vinyl-sticker-skin-96211`

New product type:

`Refrigerator Door Wraps`

New SEO title:

`Fridge Door Wrap | Vinyl Refrigerator Door Cover`

New SEO description:

`Printed vinyl fridge door wrap for smooth refrigerator or freezer fronts. Compare 6×16 to 35×87 inch sizes, measuring, preparation and installation.`

### Content changes

The page now states clearly that:

- the order contains one printed adhesive vinyl decal;
- every option specifies the finished width × height;
- available sizes run from 6 × 16 inches to 35 × 87 inches;
- the buyer must measure the flat usable panel rather than the complete appliance dimensions;
- handles, trim, displays, dispensers, hinges, seals, gaps and curved edges must be excluded from the measured area;
- ventilation openings, controls, seals, safety labels and serial information must not be covered;
- the product is not a universal pre-cut appliance skin;
- it is not a full cabinet-wrapping kit, wallpaper roll, magnetic cover or digital file;
- material for appliance sides, top, second door, freezer drawer and cabinets is not automatically included;
- compatible surfaces, installation, care and removal limitations are explained;
- custom dimensions can be reviewed before production when exact measurements and a front-facing photograph are supplied.

The description includes internal links to the Kitchen and Food & Beverages collections.

### Collection relationships

Added manually to:

- `Kitchen Stickers / Kitchen Wall Decals` — `/collections/kitchen`
- `Food & Beverages Stickers / Kitchen vinyl decals` — `/collections/food-beverages`

The product is no longer returned by the automated `Vinyl Wall Decals / Wall Stickers` collection. This was not a manual removal. That smart collection requires the product title to contain both `Wall` and `sticker`; the corrected appliance-specific title no longer satisfies the `Wall` condition. This is a relevant taxonomy correction because the product is an appliance-door wrap rather than a wall decal.

## Commercial and media integrity audit

A post-mutation GraphQL audit confirmed the following:

### Gamer wall decal

- status remains `ACTIVE`;
- handle remains `neon-game-controller-wall-decal`;
- online-store URL remains unchanged;
- 15 variants remain present;
- every variant ID, title, SKU value, price and inventory quantity remains unchanged;
- 12 media items remain present;
- every media ID, URL, dimension, order and alt value remains unchanged;
- the product remains in the Game Room and 3D Stickers collections;
- the legacy redirect remains intact.

### Refrigerator door wrap

- status remains `ACTIVE`;
- handle remains `fridge-door-wrap-vinyl-sticker-skin-96211`;
- online-store URL remains unchanged;
- 10 variants remain present;
- every variant ID, title, SKU, price and inventory quantity remains unchanged;
- 10 media items remain present;
- every media ID, URL, dimension, order and alt value remains unchanged;
- two relevant manual collection memberships were added;
- no image, price, option or inventory change was made.

Localized translations were not edited.

## Google URL Inspection

| URL | Current status | Verdict | Coverage | Indexing | Last Google crawl |
|---|---|---|---|---|---|
| `/products/neon-game-controller-wall-decal` | Indexed | PASS | Submitted and indexed | Allowed | 2026-08-26 23:51 UTC |
| `/products/fridge-door-wrap-vinyl-sticker-skin-96211` | Indexed | PASS | Submitted and indexed | Allowed | 2026-08-24 19:32 UTC |

Both crawl timestamps precede the edits made on 2026-08-30. The inspection therefore confirms that the URLs are valid and indexed, but Google has not yet processed the new titles, descriptions and page content.

## Indexing tracker after the batch

| Metric | Value |
|---|---:|
| Tracked URLs | 114 |
| Indexed | 113 |
| Not indexed | 1 |
| Pending | 0 |
| Errors | 0 |
| Warnings | 0 |

## Monitoring plan

The two URLs are now in the persistent GSC Wizard tracker. The next meaningful evaluation should compare the same query and landing-page pairs only after Google recrawls the pages and Search Console reports settled post-change data. Recently edited pages from earlier batches should not be rewritten again during that observation window.