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
# TODO: get conversion rate for ad group (p1)
# TODO: get conversion rate for PSA group (p2)
# TODO: calculate observed difference (p1 - p2)
# TODO: calculate Cohen's h effect size using proportion_effectsize()


# %% [markdown]
# ## 2. Power given actual sample sizes
#
# Given how the groups are split, what's the smallest effect we could reliably detect?

# %%
# TODO: get n1 (ad group size) and n2 (PSA group size)
# TODO: calculate the ratio n2/n1 (this is the imbalance)
# TODO: use NormalIndPower().solve_power() to find the minimum detectable effect at 80% power


# %% [markdown]
# ## 3. The imbalance problem
#
# With 588k total users but a 96/4 split, the small group is the bottleneck.
# Discuss in 3–4 sentences:
# - What would the ideal sample size split have been?
# - How does the imbalance affect what we can conclude?
# - Even with massive total N, why does this matter?

# %%
# Write your discussion as a markdown cell or print() output
