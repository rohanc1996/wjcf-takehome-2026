# D3: Hypothesis

## Statement

Districts where the empanelled-and-active supply is dominated by private facilities have lower utilisation per card than comparable public-dominated districts.

The binding constraint on use in private-dominated districts is not coverage (cards are present) but the availability of accessible, affordable care, so fewer approved claims are generated per card holder.

## Definitions

- Private-dominated: private facilities are more than half of the empanelled-and-active supply in the district.
- Public-dominated: private facilities are less than half of the empanelled-and-active supply.
- Comparable: districts in the same coverage band, so the comparison controls for how many people actually hold cards.
- Utilisation per card: approved claims at empanelled-and-active hospitals per card holder.
- Only approved claims count as use. About 55% of claims are approved, 23% rejected, 22% pending; the non-approved share never enters the metric.
- Supply is expressed relative to the eligible population (or card holders) at the small district scale used in D1. Because the synthetic districts are tiny, figures are not per 100k and are relative to this frame only, not national statistics.

## Confirm conditions

- Private-dominated districts show meaningfully lower approved claims per card than public-dominated districts within the same coverage band.
- The relationship holds when the reach-use gap is considered together with supply, not just on raw means.

## Refute conditions

- No difference in utilisation per card between the two groups once coverage is controlled for.
- The gap is explained entirely by coverage or by total supply, with composition adding nothing.

## Scope and handling of anomalous districts

- District 11 has no empanelled-and-active hospitals at all. It is excluded from the private vs public comparison and reported separately as a supply-constrained first-look district.
- District 7 enters with de-duplicated card holders (coverage around 85%), never the inflated row count. Its duplicates are investigated as a batch, not counted as real enrolment.
- District 13 enters the comparison with its true card-holder count. Its flagged coverage is a denominator problem (understated eligible population), so the inflated ratio is reported but not used as evidence for the hypothesis. Whether to keep or discard that district in the final shortlist stays open, per D1.
- Coverage is random and independent of supply in the generator, so the coverage-band control is a real check rather than a restatement of the design.
