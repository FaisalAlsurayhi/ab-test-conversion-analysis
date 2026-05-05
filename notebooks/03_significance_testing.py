# %% [markdown]
# # 03 — Significance Testing
#
# **Goal:** Run the actual tests, report the numbers properly, and discuss what they mean.
# Report effect size and CI, not just p-values. P-values alone are weak storytelling.

# %%
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from scipy.stats import chi2_contingency
from pathlib import Path

PROJECT_ROOT = Path.cwd() if Path.cwd().name != "notebooks" else Path.cwd().parent
DATA_PATH = PROJECT_ROOT / "data" / "marketing_AB.csv"

# %%
df = pd.read_csv(DATA_PATH)
df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

# %% [markdown]
# ## 1. Two-proportion z-test

# %%
# TODO: build the counts arrays
# successes = np.array([conversions_ad, conversions_psa])
# trials = np.array([n_ad, n_psa])

# TODO: run proportions_ztest(successes, trials, alternative='larger')
# TODO: print the z-statistic and p-value with interpretation


# %% [markdown]
# ## 2. Chi-square cross-check
#
# Different test, same question. If they disagree, something's off.

# %%
# TODO: build a 2x2 contingency table (group × converted)
# TODO: run chi2_contingency()
# TODO: print chi-square statistic, p-value, degrees of freedom


# %% [markdown]
# ## 3. 95% confidence interval on the difference
#
# This is the number that should anchor the recommendation.

# %%
# TODO: calculate CI for each group's conversion rate using proportion_confint()
# TODO: calculate CI for the difference in proportions
# TODO: print the difference and its CI in plain language
# Example output: "Ad group converted 0.77 percentage points higher (95% CI: 0.45 to 1.10 pp)"


# %% [markdown]
# ## 4. Selection bias — the part most people miss
#
# A statistically significant result here doesn't prove the ads caused the lift.
# Write 4–6 sentences in your own words covering:
#
# - Why the 96/4 split signals non-random group assignment
# - Concretely: who ends up in the ad group vs the PSA group, and how do they differ?
# - Why this likely overstates the true causal effect of the ad
# - What a clean follow-up test would look like (proper randomization, balanced groups, pre-registered hypothesis)

# %% [markdown]
# ## Bottom line for this notebook
#
# In one sentence: what does the test say, and how confident are you in it?
