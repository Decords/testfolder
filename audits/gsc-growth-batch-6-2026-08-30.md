# GSC growth batch 6

Date: 2026-08-30
Property: https://www.decords.com/
Settled Search Console source window: 2026-07-31 through 2026-08-27

## Decision rules

- Pages edited on 2026-08-28 or 2026-08-29 were excluded because the settled GSC window predates those changes.
- Parameterized Google product-feed variant URLs were not treated as independent organic pages or confirmed cannibalization.
- Similar products were archived only after product, variant, gallery, organic-demand and available order-record checks supported duplicate status.

## Search opportunities processed

| Search intent | Clicks | Impressions | Position | Landing page action |
|---|---:|---:|---:|---|
| makeup brush cup | 1 | 124 | 4.32 | Reframed as a physical 3D printed makeup brush cup |
| cheetah print stickers | 0 | 93 | 8.28 | Consolidated one confirmed duplicate into the established URL |
| picture frame stickers | 0 | 80 | 5.26 | Separated Our Love Story and heart-shaped photo layouts |
| custom mirror decals, extended page | 0 | 109 | 10.27 | Assigned large and multi-line personalization intent |
| custom mirror decals, compact page | 0 | 21 | 12.71 | Assigned 2–12 inch short-text intent |
| racing stripe decals | 0 | 83 | 6.74 | Reframed around vehicle fit, layout selection and required measurements |

## Shopify changes

### Active pages updated

1. Makeup Brush Cup | 3D Printed Geometric Holder
2. 50 Cheetah Print Stickers | Leopard Spot Vinyl Decal Set
3. Our Love Story Picture Frame Stickers | Gallery Wall Decal
4. Heart Picture Frame Wall Sticker | Photo Collage Decal
5. Racing Stripe Decals for Cars & Trucks | Custom Vinyl Set
6. Custom Mirror Decals | Personalized Text & Quote Sticker
7. Small Custom Mirror Decal | 2–12 Inch Text Sticker

Each active page received a differentiated visible title, structured description, product type, search-intent tags and SEO metadata. Active handles were preserved.

### Confirmed Cheetah duplicate

- Main product retained: `/products/50x-leopard-animal-skin-sticker-pack-of-cheetah-skins-print-decal-vinyl-wrap-stickers-cute-spot-art-for-girls-transfer-decals`
- Duplicate archived: product ID `gid://shopify/Product/8747418681682`
- Internal archive handle: `archived-cheetah-print-sticker-pack-03803-20260830`
- Direct redirect created from `/products/50x-leopard-animal-skin-sticker-pack-of-03803` to the retained active product.
- No matching orders were returned by the available SKU and sales searches for either duplicate.
- The established URL was retained because it held 93 of the 94 observed impressions and had the longer history.

### Collection corrections

- The retained Cheetah set was added to Bulk Stickers.
- Racing Stripes now qualifies for and appears in Car Vinyl Decals and Custom Car Sticker.
- The extended Mirror page was added to Custom & Personalized.
- The compact Mirror page automatically left the irrelevant Window Stickers collection after its title and intent were corrected.

### Cannibalization handled without deletion

- Our Love Story Picture Frame Stickers and Heart Picture Frame Wall Sticker remain active because their finished layouts are different. Reciprocal links explain the alternative designs.
- The two Mirror listings remain active because one covers 2–118 inch layouts while the other is a lower-priced compact 2–12 inch product. Reciprocal links explain which page to use.

## Controls

- Prices unchanged.
- Variants and option values unchanged.
- Inventory unchanged.
- SKU values unchanged.
- Product images and image order unchanged.
- Handles of all retained active products unchanged.
- One confirmed duplicate archived, not deleted.
- One direct URL redirect created.
- Shopify userErrors: 0.

## Indexing tracker after update

- Total tracked URLs: 94.
- Indexed: 93.
- Not indexed: 1.
- Pending: 0.
- Errors: 0.
- Warnings: 0.

The only unknown URL is the compact Mirror product. Shopify confirms that it is active, published, internally linked from the extended Mirror page and included in relevant collections. It remains in the tracker for discovery and recrawl. The other six updated active URLs are indexed and allowed for indexing.

## Deferred candidates

- Custom Mailbox Decal was not rewritten because its page was already updated on 2026-08-29 and the GSC window predates that change.
- Personalized Vinyl Text Decal was not rewritten because it was already updated on 2026-08-29 and most apparent duplicate rows were product-feed variant URLs.
- Freshly edited mask, costume, window and other collection pages remain deferred until Google recrawls them and a post-change comparison becomes available.
