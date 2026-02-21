"""
============================================================
  IPL PERFORMANCE ANALYTICS - KPI ENGINEERING MODULE
  Script: 02_kpi_engineering.py
  Author: [Your Name]
  Date:   February 2026
  Description: Calculates all 10 KPIs from cleaned IPL data
               and exports individual KPI CSVs for Power BI.
============================================================

KPIs Covered:
  1.  Team Win Percentage
  2.  Toss Impact on Match Result
  3.  Total Runs per Batsman
  4.  Strike Rate
  5.  Boundary Percentage
  6.  Bowler Economy Rate
  7.  Dot Ball Percentage
  8.  Wickets per Bowler
  9.  Venue Win Percentage
  10. Bat First vs Chase Comparison
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
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
KPI_DIR       = os.path.join(PROCESSED_DIR, "kpis")
os.makedirs(KPI_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────
# 1. LOAD CLEANED DATA
# ─────────────────────────────────────────────────────────
print("=" * 60)
print("  Loading Cleaned Datasets")
print("=" * 60)

matches    = pd.read_csv(os.path.join(PROCESSED_DIR, "matches_cleaned.csv"))
deliveries = pd.read_csv(os.path.join(PROCESSED_DIR, "deliveries_enriched.csv"))

print(f"  ✔  matches    : {matches.shape[0]:,} rows")
print(f"  ✔  deliveries : {deliveries.shape[0]:,} rows")

# ─────────────────────────────────────────────────────────
# KPI 1 — TEAM WIN PERCENTAGE
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 1: Team Win Percentage")
print("=" * 60)

# Count matches played (as team1 or team2)
team1_matches = matches.groupby("team1").size().reset_index(name="matches_as_team1")
team2_matches = matches.groupby("team2").size().reset_index(name="matches_as_team2")

team1_matches.rename(columns={"team1": "team"}, inplace=True)
team2_matches.rename(columns={"team2": "team"}, inplace=True)

total_played = pd.merge(team1_matches, team2_matches, on="team", how="outer").fillna(0)
total_played["total_matches"] = total_played["matches_as_team1"] + total_played["matches_as_team2"]

# Count wins (exclude No Result)
valid_matches = matches[matches["winner"] != "No Result"]
wins = valid_matches.groupby("winner").size().reset_index(name="total_wins")
wins.rename(columns={"winner": "team"}, inplace=True)

kpi_team_wins = pd.merge(total_played[["team", "total_matches"]], wins, on="team", how="left")
kpi_team_wins["total_wins"]      = kpi_team_wins["total_wins"].fillna(0).astype(int)
kpi_team_wins["win_percentage"]  = (
    (kpi_team_wins["total_wins"] / kpi_team_wins["total_matches"]) * 100
).round(2)
kpi_team_wins = kpi_team_wins.sort_values("win_percentage", ascending=False)

print(kpi_team_wins.to_string(index=False))
kpi_team_wins.to_csv(os.path.join(KPI_DIR, "kpi_01_team_win_percentage.csv"), index=False)
print(f"\n  ✔  Saved → kpi_01_team_win_percentage.csv")

# ─────────────────────────────────────────────────────────
# KPI 2 — TOSS IMPACT ON MATCH RESULT
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 2: Toss Impact on Match Result")
print("=" * 60)

valid = matches[matches["winner"] != "No Result"].copy()
valid["toss_won_match"] = (valid["toss_winner"] == valid["winner"]).astype(int)

# Overall toss impact
overall_toss_impact = pd.DataFrame({
    "metric": ["Toss Winner Won Match", "Toss Winner Lost Match"],
    "count" : [valid["toss_won_match"].sum(),
               len(valid) - valid["toss_won_match"].sum()]
})
overall_toss_impact["percentage"] = (
    (overall_toss_impact["count"] / len(valid)) * 100
).round(2)

# Toss impact by decision (bat / field)
toss_by_decision = valid.groupby("toss_decision").apply(
    lambda x: pd.Series({
        "total_matches"         : len(x),
        "toss_winner_won"       : x["toss_won_match"].sum(),
        "toss_win_pct"          : round(x["toss_won_match"].mean() * 100, 2)
    })
).reset_index()

# Season-wise toss impact
toss_by_season = valid.groupby("season").apply(
    lambda x: pd.Series({
        "total_matches"   : len(x),
        "toss_winner_won" : x["toss_won_match"].sum(),
        "toss_win_pct"    : round(x["toss_won_match"].mean() * 100, 2)
    })
).reset_index()

print("\n  Overall Toss Impact:")
print(overall_toss_impact.to_string(index=False))
print("\n  Toss Impact by Decision:")
print(toss_by_decision.to_string(index=False))

overall_toss_impact.to_csv(os.path.join(KPI_DIR, "kpi_02_toss_impact_overall.csv"),    index=False)
toss_by_decision.to_csv(os.path.join(KPI_DIR, "kpi_02_toss_impact_by_decision.csv"),   index=False)
toss_by_season.to_csv(os.path.join(KPI_DIR, "kpi_02_toss_impact_by_season.csv"),       index=False)
print(f"\n  ✔  Saved → kpi_02_toss_impact_*.csv")

# ─────────────────────────────────────────────────────────
# KPI 3 — TOTAL RUNS PER BATSMAN
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 3: Total Runs per Batsman")
print("=" * 60)

# batsman column may be called 'batter' in newer Kaggle versions
bat_col = "batter" if "batter" in deliveries.columns else "batsman"

kpi_batsman_runs = deliveries.groupby(bat_col).agg(
    total_runs   = ("batsman_runs", "sum"),
    innings      = ("match_id",     "nunique"),  # unique matches
    balls_faced  = ("ball",         "count"),
).reset_index()

kpi_batsman_runs.rename(columns={bat_col: "batsman"}, inplace=True)
kpi_batsman_runs = kpi_batsman_runs.sort_values("total_runs", ascending=False)

print(f"  ✔  Top 10 Run Scorers:")
print(kpi_batsman_runs.head(10).to_string(index=False))
kpi_batsman_runs.to_csv(os.path.join(KPI_DIR, "kpi_03_batsman_total_runs.csv"), index=False)
print(f"\n  ✔  Saved → kpi_03_batsman_total_runs.csv")

# ─────────────────────────────────────────────────────────
# KPI 4 — STRIKE RATE
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 4: Strike Rate")
print("=" * 60)

# Strike Rate = (Runs Scored / Balls Faced) × 100
# Exclude wides from balls faced
non_wide = deliveries[deliveries["wide_runs"] == 0]

strike_rate = non_wide.groupby(bat_col).agg(
    sr_runs        = ("batsman_runs", "sum"),
    sr_balls_faced = ("ball",         "count")
).reset_index()

strike_rate.rename(columns={bat_col: "batsman"}, inplace=True)
strike_rate["strike_rate"] = (
    (strike_rate["sr_runs"] / strike_rate["sr_balls_faced"]) * 100
).round(2)

# Filter: min 200 balls for statistical significance
strike_rate_filtered = strike_rate[strike_rate["sr_balls_faced"] >= 200].sort_values(
    "strike_rate", ascending=False
)

print(f"  ✔  Top 10 by Strike Rate (min 200 balls):")
print(strike_rate_filtered.head(10).to_string(index=False))

strike_rate.to_csv(os.path.join(KPI_DIR, "kpi_04_strike_rate.csv"), index=False)
print(f"\n  ✔  Saved → kpi_04_strike_rate.csv")

# ─────────────────────────────────────────────────────────
# KPI 5 — BOUNDARY PERCENTAGE
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 5: Boundary Percentage")
print("=" * 60)

# Boundary % = (Fours + Sixes) / Total Balls Faced × 100
boundaries = non_wide.copy()
boundaries["is_boundary"] = boundaries["batsman_runs"].isin([4, 6]).astype(int)
boundaries["is_four"]     = (boundaries["batsman_runs"] == 4).astype(int)
boundaries["is_six"]      = (boundaries["batsman_runs"] == 6).astype(int)

kpi_boundary = boundaries.groupby(bat_col).agg(
    total_balls    = ("ball",          "count"),
    fours          = ("is_four",       "sum"),
    sixes          = ("is_six",        "sum"),
    boundary_balls = ("is_boundary",   "sum"),
    boundary_runs  = ("batsman_runs",  lambda x: x[boundaries.loc[x.index, "is_boundary"] == 1].sum())
).reset_index()

kpi_boundary.rename(columns={bat_col: "batsman"}, inplace=True)
kpi_boundary["boundary_percentage"] = (
    (kpi_boundary["boundary_balls"] / kpi_boundary["total_balls"]) * 100
).round(2)

kpi_boundary_filtered = kpi_boundary[kpi_boundary["total_balls"] >= 200].sort_values(
    "boundary_percentage", ascending=False
)

print(f"  ✔  Top 10 by Boundary % (min 200 balls):")
print(kpi_boundary_filtered[["batsman", "fours", "sixes", "boundary_percentage"]].head(10).to_string(index=False))

kpi_boundary.to_csv(os.path.join(KPI_DIR, "kpi_05_boundary_percentage.csv"), index=False)
print(f"\n  ✔  Saved → kpi_05_boundary_percentage.csv")

# ─────────────────────────────────────────────────────────
# KPI 6 — BOWLER ECONOMY RATE
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 6: Bowler Economy Rate")
print("=" * 60)

# Economy Rate = Runs Conceded / Overs Bowled
# Legal deliveries only (exclude wides and no-balls for ball count)
legal_balls = deliveries[(deliveries["wide_runs"] == 0) & (deliveries["noball_runs"] == 0)]

bowler_runs  = deliveries.groupby("bowler")["total_runs"].sum().reset_index(name="runs_conceded")
bowler_balls = legal_balls.groupby("bowler")["ball"].count().reset_index(name="legal_balls")

kpi_economy = pd.merge(bowler_runs, bowler_balls, on="bowler", how="inner")
kpi_economy["overs_bowled"]  = kpi_economy["legal_balls"] / 6
kpi_economy["economy_rate"]  = (
    kpi_economy["runs_conceded"] / kpi_economy["overs_bowled"]
).round(2)

# Filter: min 10 overs for significance
kpi_economy_filtered = kpi_economy[kpi_economy["overs_bowled"] >= 10].sort_values("economy_rate")

print(f"  ✔  Top 10 Best Economy (min 10 overs):")
print(kpi_economy_filtered[["bowler", "runs_conceded", "overs_bowled", "economy_rate"]].head(10).to_string(index=False))

kpi_economy.to_csv(os.path.join(KPI_DIR, "kpi_06_economy_rate.csv"), index=False)
print(f"\n  ✔  Saved → kpi_06_economy_rate.csv")

# ─────────────────────────────────────────────────────────
# KPI 7 — DOT BALL PERCENTAGE
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 7: Dot Ball Percentage")
print("=" * 60)

# Dot ball = legal delivery where total_runs == 0
legal = deliveries[(deliveries["wide_runs"] == 0) & (deliveries["noball_runs"] == 0)].copy()
legal["is_dot"] = (legal["total_runs"] == 0).astype(int)

kpi_dot = legal.groupby("bowler").agg(
    total_legal_balls = ("ball",    "count"),
    dot_balls         = ("is_dot",  "sum")
).reset_index()

kpi_dot["dot_ball_percentage"] = (
    (kpi_dot["dot_balls"] / kpi_dot["total_legal_balls"]) * 100
).round(2)

kpi_dot_filtered = kpi_dot[kpi_dot["total_legal_balls"] >= 60].sort_values(
    "dot_ball_percentage", ascending=False
)

print(f"  ✔  Top 10 Dot Ball % (min 60 balls):")
print(kpi_dot_filtered[["bowler", "dot_balls", "total_legal_balls", "dot_ball_percentage"]].head(10).to_string(index=False))

kpi_dot.to_csv(os.path.join(KPI_DIR, "kpi_07_dot_ball_percentage.csv"), index=False)
print(f"\n  ✔  Saved → kpi_07_dot_ball_percentage.csv")

# ─────────────────────────────────────────────────────────
# KPI 8 — WICKETS PER BOWLER
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 8: Wickets per Bowler")
print("=" * 60)

# Valid dismissal kinds (not run out which is fielder's credit)
BOWLER_WICKETS = [
    "caught", "bowled", "lbw", "stumped",
    "caught and bowled", "hit wicket"
]

bowler_wickets = deliveries[
    deliveries["dismissal_kind"].isin(BOWLER_WICKETS)
].groupby("bowler").size().reset_index(name="wickets")

kpi_wickets = pd.merge(kpi_economy[["bowler", "overs_bowled"]], bowler_wickets, on="bowler", how="left")
kpi_wickets["wickets"]       = kpi_wickets["wickets"].fillna(0).astype(int)
kpi_wickets["bowling_avg"]   = np.where(
    kpi_wickets["wickets"] > 0,
    (kpi_economy["runs_conceded"] / kpi_wickets["wickets"]).round(2),
    np.nan
)
kpi_wickets = kpi_wickets.sort_values("wickets", ascending=False)

print(f"  ✔  Top 10 Wicket Takers:")
print(kpi_wickets[["bowler", "wickets", "overs_bowled", "bowling_avg"]].head(10).to_string(index=False))

kpi_wickets.to_csv(os.path.join(KPI_DIR, "kpi_08_wickets_per_bowler.csv"), index=False)
print(f"\n  ✔  Saved → kpi_08_wickets_per_bowler.csv")

# ─────────────────────────────────────────────────────────
# KPI 9 — VENUE WIN PERCENTAGE
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 9: Venue Win Percentage")
print("=" * 60)

valid_m = matches[matches["winner"] != "No Result"].copy()

venue_matches = valid_m.groupby("venue").agg(
    total_matches = ("match_id" if "match_id" in valid_m.columns else "id", "count"),
).reset_index()

# Bat first wins: team batting first (team1 in most datasets) won
# Check if win_by_runs > 0 → batting team won
bat_first_wins = valid_m[valid_m["win_by_runs"] > 0].groupby("venue").size().reset_index(name="bat_first_wins")
chase_wins     = valid_m[valid_m["win_by_wickets"] > 0].groupby("venue").size().reset_index(name="chase_wins")

kpi_venue = venue_matches.merge(bat_first_wins, on="venue", how="left")
kpi_venue = kpi_venue.merge(chase_wins, on="venue", how="left")
kpi_venue["bat_first_wins"] = kpi_venue["bat_first_wins"].fillna(0).astype(int)
kpi_venue["chase_wins"]     = kpi_venue["chase_wins"].fillna(0).astype(int)
kpi_venue["bat_first_win_pct"] = (
    (kpi_venue["bat_first_wins"] / kpi_venue["total_matches"]) * 100
).round(2)
kpi_venue["chase_win_pct"] = (
    (kpi_venue["chase_wins"] / kpi_venue["total_matches"]) * 100
).round(2)

# Total runs per venue
venue_runs = deliveries.groupby("venue")["total_runs"].sum().reset_index(name="total_runs")
kpi_venue  = kpi_venue.merge(venue_runs, on="venue", how="left")
kpi_venue["avg_runs_per_match"] = (kpi_venue["total_runs"] / kpi_venue["total_matches"]).round(1)

kpi_venue = kpi_venue[kpi_venue["total_matches"] >= 5].sort_values("total_matches", ascending=False)

print(f"  ✔  Top Venues by matches:")
print(kpi_venue[["venue", "total_matches", "bat_first_win_pct", "chase_win_pct", "avg_runs_per_match"]].head(10).to_string(index=False))

kpi_venue.to_csv(os.path.join(KPI_DIR, "kpi_09_venue_win_percentage.csv"), index=False)
print(f"\n  ✔  Saved → kpi_09_venue_win_percentage.csv")

# ─────────────────────────────────────────────────────────
# KPI 10 — BAT FIRST vs CHASE COMPARISON
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KPI 10: Bat First vs Chase Comparison")
print("=" * 60)

bat_first_total = len(valid_m[valid_m["win_by_runs"]    > 0])
chase_total     = len(valid_m[valid_m["win_by_wickets"] > 0])
total_valid     = bat_first_total + chase_total

kpi_bat_vs_chase = pd.DataFrame({
    "result_type"   : ["Bat First Win",  "Chase Win"],
    "total_wins"    : [bat_first_total,  chase_total],
    "win_percentage": [
        round(bat_first_total / total_valid * 100, 2),
        round(chase_total     / total_valid * 100, 2)
    ]
})

# Season-wise breakdown
season_bat_chase = valid_m.copy()
season_bat_chase["result_type"] = np.where(
    season_bat_chase["win_by_runs"] > 0, "Bat First", "Chase"
)
kpi_bat_chase_season = season_bat_chase.groupby(["season", "result_type"]).size().reset_index(name="wins")

print(kpi_bat_vs_chase.to_string(index=False))

kpi_bat_vs_chase.to_csv(os.path.join(KPI_DIR, "kpi_10_bat_vs_chase.csv"),              index=False)
kpi_bat_chase_season.to_csv(os.path.join(KPI_DIR, "kpi_10_bat_vs_chase_season.csv"),   index=False)
print(f"\n  ✔  Saved → kpi_10_bat_vs_chase*.csv")

# ─────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ✅  ALL KPIs GENERATED SUCCESSFULLY!")
print("=" * 60)
kpi_files = os.listdir(KPI_DIR)
for f in sorted(kpi_files):
    print(f"  📄  {f}")
print(f"\n  Total KPI files created: {len(kpi_files)}")
print("=" * 60)
