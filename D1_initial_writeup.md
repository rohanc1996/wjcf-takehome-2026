(written by me, structured and formatted by AI)

## The question

Across districts, where is scheme reach (how many eligible people hold an Ayushman card) most out of step with scheme use (how much hospitalisation those districts actually claim), and can that gap be explained by facility supply (empanelled, active hospitals)? Which districts should the NHA look at first, and is the fix more supply or more demand-side outreach?

The whole thing is district-level. I should not need any individual record to answer it, which also keeps me out of privacy trouble.

## What I need to find out

- How enrolled is each district? Card holders against the eligible population.
- How much is each district actually using? Hospitalisation claims against card holders, and against the eligible population.
- Where do those two disagree the most? Some districts will hold cards but not use them.
- Is the disagreement related to supply? Districts with fewer empanelled-and-active hospitals should show bigger gaps if supply is the binding constraint.
- Does the composition of supply matter? Private vs public-heavy districts may behave differently.

## Metrics I'm planning

- Coverage: card holders / eligible population. This needs an eligible-population figure, which is not a column in the main files. I will need a separate reference lookup by district, and I need to decide where it comes from and how to keep it aligned with the other files.
- Utilisation: claims per card holder, and per eligible person. Open decision: count all claims or only approved claims. Only approved claims represent delivered care, but I want to check what the data supports before committing.
- Supply: empanelled-and-active hospitals per 100k eligible. Open decision: per eligible or per card holder, and how to treat districts with very little supply. The PDF says I only need 5000 or so beneficiaries, so I'm going to ask the AI agent to make a reasonable population size per district accordingly (so values will not be per 100k most likely).
- Reach-use gap: some way of combining reach and use into a single ranking so the shortlist is defensible and legible.

## What I expect the data to look like, and how it will fight me (and my DeepSeek v4 Flash+OpenCode harness...)

Real Indian districts are large. Population averages around 1.8 million, ranging from 50k to 10m+, and a district has roughly 2700 hospital beds, which I take to mean around 170 facilities (I looked this up too, and turns out a facility has around 12-20 beds on average). My extract is small, a few thousand beneficiaries and claims, so the districts I model have to be shrunk to match. That means choosing district size, eligible population, and facility counts that keep the ratios realistic even though the absolute numbers are far below real India. This is a decision I need to make early, because everything downstream inherits it.

Facilities carry two independent flags: empanelment status and activity status. A hospital can be empanelled yet dormant, or active yet de-empanelled. I expect claims to reference hospitals that are not actually viable, and those must not count as real use.

Programmatic flat files tend to arrive dirty. I expect duplicate rows, impossible dates (discharge before admission), inverted or negative amounts, implausible ages, and missing identifiers or dates. Each type needs a policy: flag, drop, or correct, and I have to show the counts so the cleaning is auditable.

The brief flags the possibility of a district where recorded card holders exceed the eligible population. I do not want to just discard it, because in the real world that can happen for different reasons, and the correct response depends on the reason:

- The eligible-population number may come from 2011 census age-group figures projected forward, which can understate the true eligible count.
- Some states top up the central PM-JAY criteria with their own funds, widening eligibility beyond the central NHA count.
- Duplicate or fraudulent beneficiary entries are also possible, and those need a detection and cleaning strategy rather than being counted as real enrolment.

So a coverage ratio above 100% is not a single problem; it is a signal that something needs investigating, and the investigation differs by cause. That is a decision I need to make when I see the data: de-duplicate and investigate the IDs, or refresh the denominator, or both.

## The hypothesis I'm leaning toward

I have been curious about whether Ayushman Bharat actually made hospitalisation accessible through private hospitals. That points me at a supply-composition question: districts where the empanelled-and-active supply is dominated by private facilities might show lower utilisation per card than comparable public-dominated districts. I am not committed to it yet, and I want the confirm and refute conditions written down before I analyse.

## Decisions still to be made

- District scale: size, eligible population, and facility counts for a small synthetic extract. I'll let AI decide.
- Which claims count as use: approved only, or all claims.
- How to treat >100% coverage districts, and how to tell which cause applies before acting. Duplicates are easy, but the other possibilities I flagged above are more complex and I need to decide if I handle or discard those cases.
- Cleaning policy per dirt type, with counts shown.
- How to define the reach-use gap and rank the shortlist.
- Storage and tooling: queryable store, notebook or script, and the one-screen visual format. I want to use Streamlit since it's easier than Plotly Dash, and looks a lot nicer than basic html+css. It's also Python-based, big plus if I need to touch code directly.

## What a good answer looks like

A ranked shortlist of districts where many people hold cards but few hospitalisations are claimed, with a clear read on whether the constraint is supply or demand, plus the two anomalous coverage districts called out so nobody quotes an inflated coverage ratio as a real number. It has to be defensible at district level, honest about what synthetic, dirty data cannot support, and readable by a senior official in one screen.


## Scattered thoughts, maybe I place these somewhere later
- The PDF mentions the family and family_id as significant for claims, but I can't think of where or how this could meaningfully factor into my analysis right now.
- I want to include the data-generator script in the run-all pipeline, but if the next user changes the seed, the data will change so any hard-coded findings I report in my notebook or wherever else will mismatch. I should flag this in the readme, or not have any hard-coded findings anywhere.
- I don't need to worry about PIIs and privacy here much since it's synthetic data with numerical ids for names and families, but I should make notes of what the correct protocol would be if I was working with PIIs (anonymization, aggregation, minimum-cell-size suppression etc). I should probably also mention specific things about the DPDP or SAHI wherever relevant for brownie points.