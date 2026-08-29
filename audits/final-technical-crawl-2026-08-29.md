# Decords final technical crawl

Date: 2026-08-29
Property: https://www.decords.com/

## Scope

- 4,961 Shopify export records reviewed.
- 2,600 active products.
- 51 archived or other-status products.
- 130 collections.
- 20 published pages.
- 170 published articles.
- 1,973 URL redirects.
- 320 content sources scanned.
- 1,537 internal-link occurrences across 290 unique internal targets.
- 25 representative public pages checked for HTTP status, H1, canonical, hreflang and structured data.

## Pre-fix crawl findings

- 1,535 links already pointed directly to valid internal destinations.
- 2 content links used a valid redirect instead of the final collection URL.
- 0 unknown internal links in content.
- 0 content links to archived products.
- 0 non-canonical collection-context product links.
- 0 redirect loops.
- 28 redirect chains.
- 16 redirects required manual target review. Fourteen were valid localized or URL-encoded destinations; two genuinely pointed to the non-existing collection path /collections/door-stickers.

## Changes completed

- Replaced both content links to /collections/50-price-discount with direct links to /collections/bird-safe-window-stickers.
- Collapsed all 28 identified redirect chains to one-hop redirects.
- Corrected both invalid door-sticker targets to /collections/bathroom.
- Verified all 30 updated redirect records directly in Shopify after mutation.
- Added a redirect from /pages/customer-questions to /pages/faq.
- Added a redirect from the short Gray Kitten legacy product URL to the current active product URL.
- Updated one collection SEO title and shortened two overlong meta descriptions.
- Deleted the temporary final-crawl export file from Shopify Files.
- Preserved all legacy templates by merchant decision; no template files were deleted. The unpublished theme was renamed Legacy Templates Preserved | 29-08-2026.
- The live theme was not modified during the legacy-template decision.

## Post-fix status

- 1,537 of 1,537 scanned content-link occurrences now point directly to known internal destinations.
- 0 known content links pass through redirects.
- 0 known content links point to archived products.
- 0 known unknown internal links remain in content.
- 0 identified redirect chains remain among the audited records.
- 0 redirect loops.
- 0 Shopify userErrors in the redirect and collection updates.

## Search Console tracker

- 57 tracked URLs.
- 56 indexed.
- 1 crawled but not indexed: /pages/html-sitemap-products, an obsolete URL that redirects to the current sitemap page and is not intended to remain indexed.
- 0 pending.
- 0 errors.
- 0 warnings.

## Decision

The final technical crawl stage is complete. Core Web Vitals were not repeated because the merchant explicitly chose to retain the already optimized theme and move forward.