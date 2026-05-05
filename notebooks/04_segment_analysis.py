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
# TODO: group by (day, test group), calculate conversion rate
# TODO: plot side-by-side bar chart
# TODO: which day shows the strongest lift?


# %% [markdown]
# ## 2. Conversion by hour of day

# %%
# TODO: group by (hour, test group), calculate conversion rate
# TODO: plot line chart with both groups
# TODO: when is the audience most responsive?


# %% [markdown]
# ## 3. Conversion by ad exposure intensity
#
# This is the most important segment cut. People who saw a lot of ads also converted more —
# but is that because the ads worked, or because frequent users were always going to convert?

# %%
# TODO: bucket users by total_ads (e.g., 1-5, 6-20, 21-50, 51-100, 100+)
# TODO: calculate conversion rate per bucket within each group
# TODO: plot it
# TODO: discuss the chicken-and-egg problem — frequent users likely convert more anyway,
# regardless of whether ads caused it


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
