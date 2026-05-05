# %% [markdown]
# # 04 — Segment Analysis
#
# **Goal:** Headline lift is one number. Where is that lift actually coming from?
# Different segments often tell different stories — and the story is what gets you the recommendation.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")

PROJECT_ROOT = Path.cwd() if Path.cwd().name != "notebooks" else Path.cwd().parent
DATA_PATH = PROJECT_ROOT / "data" / "marketing_AB.csv"
VISUALS_DIR = PROJECT_ROOT / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)

# %%
df = pd.read_csv(DATA_PATH)
df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

# %% [markdown]
# ## 1. Conversion by day of week

# %%
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

day_conversion = (
    df.groupby(["most ads day", "test group"])
    .agg(users=("user id", "count"), conversion_rate=("converted", "mean"))
    .reset_index()
)
day_conversion["most ads day"] = pd.Categorical(
    day_conversion["most ads day"], categories=day_order, ordered=True
)
day_lift = day_conversion.pivot(index="most ads day", columns="test group", values="conversion_rate")
day_lift["lift_pp"] = (day_lift["ad"] - day_lift["psa"]) * 100
day_lift.sort_values("lift_pp", ascending=False)

# %%
fig, ax = plt.subplots(figsize=(9, 4.5))
sns.barplot(
    data=day_conversion.sort_values("most ads day"),
    x="most ads day",
    y="conversion_rate",
    hue="test group",
    ax=ax,
    palette=["#2f6f73", "#c77d3b"],
)
ax.set_title("Conversion rate by day")
ax.set_xlabel("Day with most ads")
ax.set_ylabel("Conversion rate")
ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.1%}")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(VISUALS_DIR / "conversion_by_day.png", dpi=150, bbox_inches="tight")
plt.show()

print("Tuesday shows the strongest raw lift, followed by Monday.")

# %% [markdown]
# ## 2. Conversion by hour of day

# %%
hour_conversion = (
    df.groupby(["most ads hour", "test group"])
    .agg(users=("user id", "count"), conversion_rate=("converted", "mean"))
    .reset_index()
)
hour_lift = hour_conversion.pivot(index="most ads hour", columns="test group", values="conversion_rate")
hour_lift["lift_pp"] = (hour_lift["ad"] - hour_lift["psa"]) * 100
hour_lift.sort_values("lift_pp", ascending=False).head(10)

# %%
fig, ax = plt.subplots(figsize=(9, 4.5))
sns.lineplot(
    data=hour_conversion,
    x="most ads hour",
    y="conversion_rate",
    hue="test group",
    marker="o",
    ax=ax,
    palette=["#2f6f73", "#c77d3b"],
)
ax.set_title("Conversion rate by hour")
ax.set_xlabel("Hour with most ads")
ax.set_ylabel("Conversion rate")
ax.set_xticks(range(0, 24, 2))
ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.1%}")
plt.tight_layout()
plt.savefig(VISUALS_DIR / "conversion_by_hour.png", dpi=150, bbox_inches="tight")
plt.show()

print("The strongest practical response window is in the afternoon/evening, especially around 14:00-20:00.")

# %% [markdown]
# ## 3. Conversion by ad exposure intensity
#
# This is the most important segment cut. People who saw a lot of ads also converted more —
# but is that because the ads worked, or because frequent users were always going to convert?

# %%
bins = [0, 5, 20, 50, 100, np.inf]
labels = ["1-5", "6-20", "21-50", "51-100", "100+"]
df["ad_exposure_bucket"] = pd.cut(df["total ads"], bins=bins, labels=labels)

exposure_conversion = (
    df.groupby(["ad_exposure_bucket", "test group"], observed=False)
    .agg(users=("user id", "count"), conversion_rate=("converted", "mean"))
    .reset_index()
)
exposure_lift = exposure_conversion.pivot(
    index="ad_exposure_bucket", columns="test group", values="conversion_rate"
)
exposure_lift["lift_pp"] = (exposure_lift["ad"] - exposure_lift["psa"]) * 100
exposure_lift

# %%
fig, ax = plt.subplots(figsize=(9, 4.5))
sns.lineplot(
    data=exposure_conversion,
    x="ad_exposure_bucket",
    y="conversion_rate",
    hue="test group",
    marker="o",
    ax=ax,
    palette=["#2f6f73", "#c77d3b"],
)
ax.set_title("Conversion rate by exposure intensity")
ax.set_xlabel("Total ads seen")
ax.set_ylabel("Conversion rate")
ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")
plt.tight_layout()
plt.savefig(VISUALS_DIR / "conversion_by_exposure.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# Conversion rises sharply with total ad exposure, especially after 50 ads. I would not read that as proof that more ads caused more conversions, because frequent users had more chances to see ads and may have been more likely to convert anyway. The exposure cut is useful for targeting and follow-up design, but it is also the most confounded view in the analysis.

# %% [markdown]
# ## 4. Where would you double down?
#
# Based on the segment cuts, where should the marketing team focus?
# This is what feeds the recommendation in the README.
#
# Write 4–6 sentences covering:
# - Which segment shows the strongest, most defensible lift?
# - Which segments look promising but are likely confounded?
# - What would you tell the marketing team to do Monday morning?

# %% [markdown]
# I would focus Monday morning on the day and time windows where the lift is strong and the sample size is still credible: Tuesday and Monday, with afternoon/evening hours getting the first look. The exposure-intensity story is tempting because high-exposure users convert much more, but that is also where reverse causality and engagement bias are loudest. Users who are already active see more ads, so the campaign may be chasing intent rather than creating it. My recommendation would be to keep the current campaign as a directional signal, then run a properly randomized follow-up that tests the best day/hour windows with balanced treatment and control groups.
