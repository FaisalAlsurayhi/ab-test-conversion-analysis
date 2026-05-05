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
# TODO: count users in each test group
# TODO: calculate the percentage split
# TODO: note the imbalance — this is the headline of the whole story


# %% [markdown]
# ## 2. Conversion rate by group
#
# The naive comparison. Don't draw conclusions yet — just observe.

# %%
# TODO: calculate conversion rate for each group
# TODO: calculate the absolute and relative lift


# %% [markdown]
# ## 3. Exposure patterns
#
# When did people see ads, and how many? This sets up the segment analysis later.

# %%
# TODO: distribution of total ads seen
# TODO: distribution by day of week
# TODO: distribution by hour of day


# %% [markdown]
# ## 4. Save key visuals
#
# Export 2–3 charts to /visuals so the README can reference them.

# %%
# TODO: save group composition chart
# TODO: save conversion rate comparison chart
# TODO: save exposure distribution chart


# %% [markdown]
# ## Observations
#
# Write 3–5 sentences in your own words about what you saw.
# What surprised you? What's the most important thing to flag for the next notebook?
