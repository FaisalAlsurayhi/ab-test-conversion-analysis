# A/B Test Conversion Analysis

> **Business question:** Did the ad campaign drive enough lift in conversion to justify scaling the spend?

## TL;DR

The ad group converted at **2.55%** versus **1.79%** for the PSA group. That is a **0.77 percentage-point lift**, or about **43% higher** than PSA.

That looks good at first glance, but I would not call this a clean win yet. The test split was roughly **96% ad / 4% PSA**, which makes me cautious about how users were assigned. My read: the campaign is worth a cleaner follow-up test, but I would not scale spend hard from this result alone.

## Dataset

- **Source:** [Marketing A/B Testing - Kaggle](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing)
- **Size:** 588,101 rows
- **Columns:** user id, test group (ad/psa), converted (bool), total ads, most ads day, most ads hour
- **Known limitation:** group assignment is heavily imbalanced, which limits causal inference

## Approach

- Checked the basics first: row count, missing values, group sizes, and conversion rates.
- Compared conversion for ad users against PSA users.
- Ran a one-sided two-proportion z-test and checked the result with chi-square.
- Calculated a confidence interval for the lift, because the size of the effect matters more than just "significant or not."
- Looked at day, hour, and exposure cuts to see where the lift was coming from.

## Key Findings

- **The ad group converted higher:** ad users converted at **2.55%** vs **1.79%** for PSA, a **0.77 percentage-point lift**.
- **The result is statistically strong:** the one-sided z-test returned **z = 7.37** and **p = 8.53e-14**. The chi-square check told the same story with **p = 1.71e-13**.
- **The lift is not just noise:** the 95% confidence interval is **0.60 to 0.94 percentage points**.
- **The split is the part I do not love:** **564,577 users** were in the ad group and only **23,524** were in PSA. That kind of imbalance makes selection bias a real concern.
- **Timing patterns hint at useful follow-up targets:** Tuesday had the strongest raw day-level lift, followed by Monday, and afternoon/evening hours also looked promising. I would still treat those cuts as directional because the same selection issue applies.

## Recommendation

I would not scale spend aggressively off this test alone. The campaign looks promising, but the assignment pattern is too lopsided for me to treat the observed lift as a clean causal effect.

The next move is a cleaner follow-up test. I would randomly assign users before exposure, use a more balanced treatment/control split, define the conversion window up front, and focus the test around the strongest day and hour windows from this analysis. If that follow-up reproduces even part of the 0.77 percentage-point lift, scaling becomes a much easier call.

## Limitations

- The biggest issue is selection bias. The groups may not have been randomly assigned, so the observed lift could be overstating the true campaign effect.
- Timing is limited to day and hour. That is useful, but not enough to fully separate campaign timing from audience behavior.
- The conversion field is binary, so I cannot tell whether the ad group brought in higher-value customers or just more customers.
- Exposure intensity is messy: frequent users see more ads, and those same users may have been more likely to convert anyway.

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

# Download marketing_AB.csv from the Kaggle link above and place it in data/
# Then run the notebooks in order: 01 -> 02 -> 03 -> 04
```

## Visuals

![Conversion by group](visuals/conversion_by_group.png)

![Conversion by exposure intensity](visuals/conversion_by_exposure.png)

![Conversion by day](visuals/conversion_by_day.png)

---

*Built by Faisal Alsurayhi as part of a data analyst portfolio focused on Saudi Arabia's Eastern Province market.*
