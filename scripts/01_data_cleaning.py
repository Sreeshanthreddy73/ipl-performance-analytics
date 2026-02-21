"""
============================================================
  IPL PERFORMANCE ANALYTICS - DATA CLEANING MODULE
  Script: 01_data_cleaning.py
  Author: [Your Name]
  Date:   February 2026
  Description: Cleans and preprocesses IPL matches.csv and
               deliveries.csv for downstream KPI engineering
               and Power BI dashboarding.
============================================================
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────
# 0. CONFIGURATION
# ─────────────────────────────────────────────────────────
RAW_DIR       = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

MATCHES_FILE    = os.path.join(RAW_DIR, "matches.csv")
DELIVERIES_FILE = os.path.join(RAW_DIR, "deliveries.csv")

# ─────────────────────────────────────────────────────────
# 1. LOAD RAW DATA
# ─────────────────────────────────────────────────────────
print("=" * 60)
print("  STEP 1: Loading Raw Data")
print("=" * 60)

matches    = pd.read_csv(MATCHES_FILE)
deliveries = pd.read_csv(DELIVERIES_FILE)

print(f"  ✔  matches.csv    loaded  → {matches.shape[0]:,} rows × {matches.shape[1]} cols")
print(f"  ✔  deliveries.csv loaded  → {deliveries.shape[0]:,} rows × {deliveries.shape[1]} cols")

# ─────────────────────────────────────────────────────────
# 2. STANDARDIZE TEAM NAMES
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 2: Standardizing Team Names")
print("=" * 60)

TEAM_NAME_MAP = {
    # Franchise renames / historical variants
    "Delhi Daredevils"               : "Delhi Capitals",
    "Deccan Chargers"                : "Sunrisers Hyderabad",
    "Rising Pune Supergiants"        : "Rising Pune Supergiant",
    "Rising Pune Supergiants"        : "Rising Pune Supergiant",
    "Kings XI Punjab"                : "Punjab Kings",
    "Pune Warriors"                  : "Pune Warriors India",
    "Kochi Tuskers Kerala"           : "Kochi Tuskers Kerala",
    # Typo corrections
    "Royal Challengers Bangaloru"    : "Royal Challengers Bangalore",
}

team_cols_matches    = ["team1", "team2", "toss_winner", "winner"]
team_cols_deliveries = ["batting_team", "bowling_team"]

for col in team_cols_matches:
    if col in matches.columns:
        matches[col] = matches[col].replace(TEAM_NAME_MAP)

for col in team_cols_deliveries:
    if col in deliveries.columns:
        deliveries[col] = deliveries[col].replace(TEAM_NAME_MAP)

print(f"  ✔  Team name standardization applied to {len(team_cols_matches)} match cols "
      f"and {len(team_cols_deliveries)} delivery cols")

# ─────────────────────────────────────────────────────────
# 3. HANDLE MISSING VALUES – MATCHES
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 3: Handling Missing Values")
print("=" * 60)

print("\n  [matches.csv] Null counts BEFORE:")
print(matches.isnull().sum()[matches.isnull().sum() > 0].to_string())

# 'winner' is null for tied / no-result matches – fill with "No Result"
matches["winner"]           = matches["winner"].fillna("No Result")
matches["player_of_match"]  = matches["player_of_match"].fillna("N/A")
matches["city"]             = matches["city"].fillna(matches["venue"].apply(
                                  lambda v: v.split(",")[0] if isinstance(v, str) else "Unknown"))
matches["umpire1"]          = matches["umpire1"].fillna("Unknown")
matches["umpire2"]          = matches["umpire2"].fillna("Unknown")
matches["umpire3"]          = matches["umpire3"].fillna("Unknown")

print("\n  [matches.csv] Null counts AFTER:")
remaining = matches.isnull().sum()[matches.isnull().sum() > 0]
print(remaining.to_string() if len(remaining) else "  → No missing values remain!")

print("\n  [deliveries.csv] Null counts BEFORE:")
print(deliveries.isnull().sum()[deliveries.isnull().sum() > 0].to_string())

# Numeric fill – runs / wicket extras
fill_zero_cols = [
    "wide_runs", "bye_runs", "legbye_runs", "noball_runs",
    "penalty_runs", "batsman_runs", "extra_runs", "total_runs"
]
for col in fill_zero_cols:
    if col in deliveries.columns:
        deliveries[col] = deliveries[col].fillna(0)

# Dismissal type is NaN when batter is not out – valid, leave as is but document
deliveries["dismissal_kind"] = deliveries["dismissal_kind"].fillna("not out")
deliveries["player_dismissed"] = deliveries["player_dismissed"].fillna("N/A")
deliveries["fielder"]          = deliveries["fielder"].fillna("N/A")

print("\n  [deliveries.csv] Null counts AFTER:")
remaining_d = deliveries.isnull().sum()[deliveries.isnull().sum() > 0]
print(remaining_d.to_string() if len(remaining_d) else "  → No missing values remain!")

# ─────────────────────────────────────────────────────────
# 4. DATE FORMAT CONVERSION
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 4: Converting Date Formats")
print("=" * 60)

matches["date"] = pd.to_datetime(matches["date"], infer_datetime_format=True, errors="coerce")
matches["year"] = matches["date"].dt.year
matches["month"] = matches["date"].dt.month
matches["month_name"] = matches["date"].dt.month_name()
matches["season"] = matches["year"]          # alias for Power BI

print(f"  ✔  Date range: {matches['date'].min().date()} → {matches['date'].max().date()}")
print(f"  ✔  Seasons covered: {sorted(matches['season'].unique())}")

# ─────────────────────────────────────────────────────────
# 5. REMOVE DUPLICATES
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 5: Removing Duplicates")
print("=" * 60)

before_m = len(matches)
matches = matches.drop_duplicates()
print(f"  ✔  matches.csv    : {before_m - len(matches)} duplicate rows dropped → {len(matches):,} remain")

before_d = len(deliveries)
deliveries = deliveries.drop_duplicates()
print(f"  ✔  deliveries.csv : {before_d - len(deliveries)} duplicate rows dropped → {len(deliveries):,} remain")

# ─────────────────────────────────────────────────────────
# 6. FEATURE ENGINEERING ON MATCHES
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 6: Feature Engineering")
print("=" * 60)

# Toss win = match win flag
matches["toss_win_match_win"] = (matches["toss_winner"] == matches["winner"]).astype(int)

# Result type flag
matches["is_no_result"] = (matches["winner"] == "No Result").astype(int)

# Rename id → match_id for clarity
if "id" in matches.columns:
    matches.rename(columns={"id": "match_id"}, inplace=True)

print("  ✔  toss_win_match_win column created")
print("  ✔  is_no_result column created")

# ─────────────────────────────────────────────────────────
# 7. MERGE DATASETS
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 7: Merging Datasets")
print("=" * 60)

# Match the foreign key name in deliveries
del_fk = "match_id" if "match_id" in deliveries.columns else "id"

# Bring season, venue, city into deliveries
merge_cols = ["match_id" if "match_id" in matches.columns else "id",
              "season", "venue", "city", "date", "toss_winner",
              "toss_decision", "winner", "toss_win_match_win"]
merge_cols = [c for c in merge_cols if c in matches.columns]

deliveries_enriched = deliveries.merge(
    matches[merge_cols],
    left_on  = del_fk,
    right_on = "match_id" if "match_id" in matches.columns else "id",
    how      = "left"
)

print(f"  ✔  Merged dataset shape: {deliveries_enriched.shape[0]:,} rows × {deliveries_enriched.shape[1]} cols")

# ─────────────────────────────────────────────────────────
# 8. EXPORT CLEANED DATASETS
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 8: Exporting Cleaned Datasets")
print("=" * 60)

matches.to_csv(os.path.join(PROCESSED_DIR, "matches_cleaned.csv"),    index=False)
deliveries.to_csv(os.path.join(PROCESSED_DIR, "deliveries_cleaned.csv"), index=False)
deliveries_enriched.to_csv(os.path.join(PROCESSED_DIR, "deliveries_enriched.csv"), index=False)

print(f"  ✔  matches_cleaned.csv      → {PROCESSED_DIR}")
print(f"  ✔  deliveries_cleaned.csv   → {PROCESSED_DIR}")
print(f"  ✔  deliveries_enriched.csv  → {PROCESSED_DIR}")

print("\n" + "=" * 60)
print("  DATA CLEANING COMPLETE!")
print("=" * 60)
