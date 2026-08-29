# Decords Google Search Console final review

Date: 2026-08-29
Property: https://www.decords.com/

## Starting tracker state

- 57 tracked URLs.
- 56 indexed URLs.
- 1 URL marked as not indexed.
- 0 pending URLs.
- 0 errors.
- 0 warnings.

The only not-indexed URL was `/pages/html-sitemap-products`. URL Inspection identified it as an obsolete legacy address rather than a current page that should retain an independent Google index entry. It redirects to the current sitemap page.

## Actions completed

- Removed `/pages/html-sitemap-products` from the indexing tracker so the monitoring report no longer treats the obsolete redirect as a current indexing problem.
- Rechecked the tracker after removal. No meaningful current URL remained under the `not_indexed` filter.
- Rechecked the tracker filters for errors, warnings and pending URLs.
- Inspected the active homepage, `/pages/faq` and `/pages/sitemap` through the Search Console integration.
- Ensured the homepage, FAQ page and current sitemap page are included in monitoring.
- Checked the submitted Shopify sitemap at `/sitemap.xml` and its Search Console performance record.
- Requested fresh monitoring checks for the active canonical pages.
- Sent discovery notifications for the homepage, FAQ and current sitemap page through the available indexing notification workflow.

## Result

- The earlier `Crawled - currently not indexed` signal was a monitoring false positive caused by an obsolete redirect URL.
- No current indexable page requires a content, canonical, redirect or robots change as a result of this review.
- No active indexing error, warning or pending issue was found in the monitored set after cleanup.
- The old sitemap-products address should remain a redirect and should not be forced back into Google’s index.
- The current Shopify sitemap remains the correct discovery source.

## Next phase started

The technical indexing stage is closed. The performance-growth stage has started with the following Search Console datasets:

- Query performance for the last 90 days.
- Page performance for the last 90 days.
- Queries and pages with at least 20 impressions for opportunity screening.
- Ranking changes for the latest 30 days compared with the preceding 30 days.

The next workstream is to prioritize:

1. High-impression queries with weak CTR.
2. Queries ranking in positions 4–20.
3. Pages losing clicks, impressions or average position.
4. Pages receiving impressions for mismatched search intent.
5. Cannibalization where several Decords URLs compete for the same query.
