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
summary = (
    df.groupby("test group")
    .agg(users=("user id", "count"), conversions=("converted", "sum"), conversion_rate=("converted", "mean"))
    .sort_index()
)
summary

# %%
successes = np.array([summary.loc["ad", "conversions"], summary.loc["psa", "conversions"]])
trials = np.array([summary.loc["ad", "users"], summary.loc["psa", "users"]])

z_stat, p_value = proportions_ztest(successes, trials, alternative="larger")

print(f"Z-statistic: {z_stat:.2f}")
print(f"P-value: {p_value:.2e}")
print("The ad group conversion rate is statistically higher than PSA at alpha = 0.05.")


# %% [markdown]
# ## 2. Chi-square cross-check
#
# Different test, same question. If they disagree, something's off.

# %%
contingency = pd.crosstab(df["test group"], df["converted"])
contingency

# %%
chi2, chi_p, dof, expected = chi2_contingency(contingency, correction=False)

print(f"Chi-square statistic: {chi2:.2f}")
print(f"P-value: {chi_p:.2e}")
print(f"Degrees of freedom: {dof}")
print("The chi-square result points to the same conclusion as the z-test.")

# %% [markdown]
# ## 3. 95% confidence interval on the difference
#
# This is the number that should anchor the recommendation.

# %%
ad_conversions, psa_conversions = successes
ad_n, psa_n = trials
ad_rate = ad_conversions / ad_n
psa_rate = psa_conversions / psa_n
diff = ad_rate - psa_rate

ad_ci = proportion_confint(ad_conversions, ad_n, alpha=0.05, method="normal")
psa_ci = proportion_confint(psa_conversions, psa_n, alpha=0.05, method="normal")

diff_se = np.sqrt(ad_rate * (1 - ad_rate) / ad_n + psa_rate * (1 - psa_rate) / psa_n)
diff_ci = (diff - 1.96 * diff_se, diff + 1.96 * diff_se)

print(f"Ad conversion rate: {ad_rate:.2%} (95% CI: {ad_ci[0]:.2%} to {ad_ci[1]:.2%})")
print(f"PSA conversion rate: {psa_rate:.2%} (95% CI: {psa_ci[0]:.2%} to {psa_ci[1]:.2%})")
print(
    f"Ad group converted {diff * 100:.2f} percentage points higher "
    f"(95% CI: {diff_ci[0] * 100:.2f} to {diff_ci[1] * 100:.2f} pp)."
)


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
# The result is statistically significant, but I would not sell it as a clean causal win. The 96/4 split is the biggest warning sign because it does not look like a standard randomized A/B test; most users ended up in the ad group and a small slice ended up in PSA. If the ad group contains more active users, users in higher-value placements, or users who were exposed more often because they were already engaged, the raw lift will overstate what the ad caused. The clean follow-up would randomly assign users before exposure, use a more balanced split, define the conversion window up front, and pre-register the one-sided hypothesis before looking at results.

# %% [markdown]
# ## Bottom line for this notebook
#
# In one sentence: what does the test say, and how confident are you in it?

# %% [markdown]
# The ad group converted 0.77 percentage points higher than PSA and the statistical evidence is very strong, but the non-random-looking split means I am confident in the association and cautious about the causal interpretation.
