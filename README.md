# A/B Test Conversion Analysis

> **Business question:** Did the ad campaign drive enough lift in conversion to justify scaling the spend?

## TL;DR Finding
<!-- Write 2–3 sentences after you finish the analysis. Lead with the headline number and the recommendation. -->
<!-- Example shape: "The ad group converted at X% vs Y% for the PSA group — a Z percentage-point lift. However, the groups weren't randomly assigned (96% / 4% split), so I'd treat the headline lift as an upper bound and recommend a properly randomized follow-up before scaling spend." -->

## Dataset
- **Source:** [Marketing A/B Testing — Kaggle](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing)
- **Size:** ~588k rows
- **Columns:** user id, test group (ad/psa), converted (bool), total ads, most ads day, most ads hour
- **Known limitation:** group assignment is heavily imbalanced (~96% ad / ~4% PSA), which limits causal inference

## Approach
<!-- 3–5 plain-English bullets describing what you actually did. No jargon. -->
- Exploratory analysis to understand group composition and exposure patterns
- Stated hypotheses and ran a power analysis to size up minimum detectable effect
- Two-proportion z-test on conversion rate, cross-checked with chi-square
- Segment analysis by day, hour, and exposure intensity
- Discussed selection bias and what a clean follow-up test would look like

## Key Findings
<!-- 3–4 bullets with specific numbers. Lead each with the finding, not the method. -->
- Finding 1: ...
- Finding 2: ...
- Finding 3: ...

## Recommendation
<!-- What should the marketing team actually do? Write this like a memo to a manager, not a research conclusion. -->

## Limitations
- Selection bias: groups weren't randomly assigned, so observed lift likely overstates true causal effect
- No timestamp granularity beyond day/hour — can't fully separate novelty effects
- Conversion definition is binary; we don't see purchase value or downstream LTV

## Reproducibility
```bash
# Clone the repo
git clone https://github.com/FaisalAlsurayhi/ab-test-conversion-analysis.git
cd ab-test-conversion-analysis

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download the dataset from Kaggle and place in data/
# Then run the notebooks in order: 01 → 02 → 03 → 04
```

## Screenshots
<!-- Embed 2–3 of the key visuals from /visuals after you generate them. -->
<!-- ![Conversion by group](visuals/conversion_by_group.png) -->

---
*Built by Faisal Alsurayhi as part of a data analyst portfolio focused on Saudi Arabia's Eastern Province market.*
