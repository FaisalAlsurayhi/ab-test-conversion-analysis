# %% [markdown]
# # 01 — Exploratory Data Analysis
#
# **Goal:** Understand what we're working with before testing anything.
# By the end of this notebook you should be able to answer:
# - How big is each group?
# - What does the conversion rate look like?
# - Where is the imbalance, and why does it matter?

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
pd.set_option("display.max_columns", None)

PROJECT_ROOT = Path.cwd() if Path.cwd().name != "notebooks" else Path.cwd().parent
DATA_PATH = PROJECT_ROOT / "data" / "marketing_AB.csv"
VISUALS_DIR = PROJECT_ROOT / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)

# %% [markdown]
# ## Load data

# %%
df = pd.read_csv(DATA_PATH)
df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
df.head()

# %%
# Quick health check
print(f"Rows: {len(df):,}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nDtypes:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# %% [markdown]
# ## 1. Group composition
#
# How many users in each test group? This is the first place imbalance shows up.

# %%
group_counts = (
    df["test group"]
    .value_counts()
    .rename_axis("test_group")
    .reset_index(name="users")
)
group_counts["share"] = group_counts["users"] / group_counts["users"].sum()
group_counts

# %%
print(
    f"Ad group: {group_counts.loc[group_counts['test_group'] == 'ad', 'users'].iloc[0]:,} users "
    f"({group_counts.loc[group_counts['test_group'] == 'ad', 'share'].iloc[0]:.1%})"
)
print(
    f"PSA group: {group_counts.loc[group_counts['test_group'] == 'psa', 'users'].iloc[0]:,} users "
    f"({group_counts.loc[group_counts['test_group'] == 'psa', 'share'].iloc[0]:.1%})"
)
print("The split is about 96/4, so the PSA group is the bottleneck for inference.")

# %% [markdown]
# ## 2. Conversion rate by group
#
# The naive comparison. Don't draw conclusions yet — just observe.

# %%
conversion_summary = (
    df.groupby("test group")
    .agg(
        users=("user id", "count"),
        conversions=("converted", "sum"),
        conversion_rate=("converted", "mean"),
        median_ads=("total ads", "median"),
        mean_ads=("total ads", "mean"),
    )
    .sort_index()
)
conversion_summary

# %%
ad_rate = conversion_summary.loc["ad", "conversion_rate"]
psa_rate = conversion_summary.loc["psa", "conversion_rate"]
absolute_lift = ad_rate - psa_rate
relative_lift = ad_rate / psa_rate - 1

print(f"Ad conversion rate: {ad_rate:.2%}")
print(f"PSA conversion rate: {psa_rate:.2%}")
print(f"Absolute lift: {absolute_lift * 100:.2f} percentage points")
print(f"Relative lift: {relative_lift:.1%}")

# %% [markdown]
# ## 3. Exposure patterns
#
# When did people see ads, and how many? This sets up the segment analysis later.

# %%
df["total ads"].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95, 0.99])

# %%
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_summary = (
    df.groupby(["most ads day", "test group"])
    .agg(users=("user id", "count"), conversion_rate=("converted", "mean"))
    .reset_index()
)
day_summary["most ads day"] = pd.Categorical(
    day_summary["most ads day"], categories=day_order, ordered=True
)
day_summary.sort_values(["most ads day", "test group"]).head(14)

# %%
hour_summary = (
    df.groupby(["most ads hour", "test group"])
    .agg(users=("user id", "count"), conversion_rate=("converted", "mean"))
    .reset_index()
)
hour_summary.head()

# %% [markdown]
# ## 4. Save key visuals
#
# Export 2–3 charts to /visuals so the README can reference them.

# %%
fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=group_counts, x="test_group", y="users", ax=ax, palette=["#2f6f73", "#c77d3b"])
ax.set_title("A/B test group sizes")
ax.set_xlabel("Test group")
ax.set_ylabel("Users")
for patch, share in zip(ax.patches, group_counts["share"]):
    ax.annotate(
        f"{share:.1%}",
        (patch.get_x() + patch.get_width() / 2, patch.get_height()),
        ha="center",
        va="bottom",
    )
plt.tight_layout()
plt.savefig(VISUALS_DIR / "group_composition.png", dpi=150, bbox_inches="tight")
plt.show()

# %%
conversion_plot = conversion_summary.reset_index()
fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(
    data=conversion_plot,
    x="test group",
    y="conversion_rate",
    ax=ax,
    palette=["#2f6f73", "#c77d3b"],
)
ax.set_title("Conversion rate by test group")
ax.set_xlabel("Test group")
ax.set_ylabel("Conversion rate")
ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.1%}")
for patch, rate in zip(ax.patches, conversion_plot["conversion_rate"]):
    ax.annotate(
        f"{rate:.2%}",
        (patch.get_x() + patch.get_width() / 2, patch.get_height()),
        ha="center",
        va="bottom",
    )
plt.tight_layout()
plt.savefig(VISUALS_DIR / "conversion_by_group.png", dpi=150, bbox_inches="tight")
plt.show()

# %%
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df["total ads"].clip(upper=100), bins=40, ax=ax, color="#5b7f95")
ax.set_title("Distribution of ad exposure, capped at 100 ads")
ax.set_xlabel("Total ads seen")
ax.set_ylabel("Users")
plt.tight_layout()
plt.savefig(VISUALS_DIR / "ad_exposure_distribution.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## Observations
#
# Write 3–5 sentences in your own words about what you saw.
# What surprised you? What's the most important thing to flag for the next notebook?

# %% [markdown]
# The first thing that stands out is the group split: about 96% of users are in the ad group and only 4% are in the PSA group. The ad group converts at 2.55% versus 1.79% for PSA, which is a 0.77 percentage-point lift and a 43.1% relative lift. Exposure patterns look similar on average, with both groups seeing a median of about 12-13 ads, but total ad exposure is very skewed. The imbalance is the main issue to carry forward: the lift is real in the raw data, but the assignment pattern makes me cautious about treating it as clean causal evidence.
