# %% [markdown]
# # 02 — Hypothesis and Power
#
# **Goal:** State what we're testing and check whether the data can actually answer it.
# Most analysts skip the power step. Don't.

# %%
import pandas as pd
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
from pathlib import Path

PROJECT_ROOT = Path.cwd() if Path.cwd().name != "notebooks" else Path.cwd().parent
DATA_PATH = PROJECT_ROOT / "data" / "marketing_AB.csv"

# %%
df = pd.read_csv(DATA_PATH)
df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

# %% [markdown]
# ## Hypotheses
#
# **H₀:** Conversion rate is the same for the ad group and the PSA group.
#
# **H₁:** Conversion rate is higher for the ad group than the PSA group.
#
# **Significance level:** α = 0.05 (one-sided)
#
# **Why one-sided:** the marketing team only cares whether ads *increased* conversion. A decrease wouldn't change the decision (they'd kill the campaign either way).

# %% [markdown]
# ## 1. Observed effect size
#
# Calculate the actual conversion rates and the difference between groups.

# %%
summary = (
    df.groupby("test group")
    .agg(users=("user id", "count"), conversions=("converted", "sum"), conversion_rate=("converted", "mean"))
    .sort_index()
)
summary

# %%
p1 = summary.loc["ad", "conversion_rate"]
p2 = summary.loc["psa", "conversion_rate"]
observed_diff = p1 - p2
effect_size = proportion_effectsize(p1, p2)

print(f"Ad conversion rate: {p1:.2%}")
print(f"PSA conversion rate: {p2:.2%}")
print(f"Observed difference: {observed_diff * 100:.2f} percentage points")
print(f"Cohen's h: {effect_size:.4f}")

# %% [markdown]
# ## 2. Power given actual sample sizes
#
# Given how the groups are split, what's the smallest effect we could reliably detect?

# %%
n1 = summary.loc["ad", "users"]
n2 = summary.loc["psa", "users"]
ratio = n2 / n1

power_analysis = NormalIndPower()
observed_power = power_analysis.power(
    effect_size=effect_size,
    nobs1=n1,
    alpha=0.05,
    ratio=ratio,
    alternative="larger",
)

mde_h = power_analysis.solve_power(
    effect_size=None,
    nobs1=n1,
    alpha=0.05,
    power=0.80,
    ratio=ratio,
    alternative="larger",
)

# Convert Cohen's h back to an approximate percentage-point lift around the PSA baseline.
mde_rate = np.sin(np.arcsin(np.sqrt(p2)) + mde_h / 2) ** 2
mde_pp = mde_rate - p2

print(f"Ad users: {n1:,}")
print(f"PSA users: {n2:,}")
print(f"Sample-size ratio (PSA/ad): {ratio:.4f}")
print(f"Observed power: {observed_power:.3f}")
print(f"Minimum detectable effect at 80% power: {mde_pp * 100:.2f} percentage points")


# %% [markdown]
# ## 3. The imbalance problem
#
# With 588k total users but a 96/4 split, the small group is the bottleneck.
# Discuss in 3–4 sentences:
# - What would the ideal sample size split have been?
# - How does the imbalance affect what we can conclude?
# - Even with massive total N, why does this matter?

# %%
# %% [markdown]
# A cleaner experiment would have used a balanced or near-balanced split, because the smaller PSA group controls the precision of the comparison. Here, the total sample is huge, but only 23,524 users are in the PSA group, so the effective comparison is much smaller than the headline 588k rows suggests. The observed lift is large enough that the test is still highly powered, but the 96/4 split is a warning sign about assignment quality. Power tells me the dataset can detect small differences; it does not solve the bigger problem that users may not have been randomly assigned.
