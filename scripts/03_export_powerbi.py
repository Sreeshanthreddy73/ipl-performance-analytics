"""
============================================================
  IPL PERFORMANCE ANALYTICS - POWER BI EXPORT MODULE
  Script: 03_export_powerbi.py
  Author: [Your Name]
  Date:   February 2026
  Description: Consolidates all cleaned data and KPI tables
               into a single Excel workbook (.xlsx) and
               individual CSVs — ready to import into Power BI.
============================================================

Output Files:
  ├── data/processed/
  │   └── IPL_PowerBI_Master.xlsx    ← Main file for Power BI
  │       ├── Sheet: Matches
  │       ├── Sheet: Deliveries
  │       ├── Sheet: KPI_TeamWins
  │       ├── Sheet: KPI_TossImpact
  │       ├── Sheet: KPI_BatsmanRuns
  │       ├── Sheet: KPI_StrikeRate
  │       ├── Sheet: KPI_Boundary
  │       ├── Sheet: KPI_Economy
  │       ├── Sheet: KPI_DotBall
  │       ├── Sheet: KPI_Wickets
  │       ├── Sheet: KPI_Venue
  │       └── Sheet: KPI_BatVsChase
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
OUTPUT_EXCEL  = os.path.join(PROCESSED_DIR, "IPL_PowerBI_Master.xlsx")

print("=" * 60)
print("  IPL Analytics — Power BI Export")
print("=" * 60)

# ─────────────────────────────────────────────────────────
# 1. LOAD CLEANED DATASETS
# ─────────────────────────────────────────────────────────
print("\n  [1/4] Loading cleaned datasets...")

matches    = pd.read_csv(os.path.join(PROCESSED_DIR, "matches_cleaned.csv"))
deliveries = pd.read_csv(os.path.join(PROCESSED_DIR, "deliveries_enriched.csv"))

print(f"  ✔  matches    → {matches.shape[0]:,} rows")
print(f"  ✔  deliveries → {deliveries.shape[0]:,} rows")

# ─────────────────────────────────────────────────────────
# 2. LOAD ALL KPI FILES
# ─────────────────────────────────────────────────────────
print("\n  [2/4] Loading KPI tables...")

kpi_files = {
    "KPI_TeamWins"   : "kpi_01_team_win_percentage.csv",
    "KPI_TossImpact" : "kpi_02_toss_impact_overall.csv",
    "KPI_TossSeason" : "kpi_02_toss_impact_by_season.csv",
    "KPI_TossDec"    : "kpi_02_toss_impact_by_decision.csv",
    "KPI_BatsmanRuns": "kpi_03_batsman_total_runs.csv",
    "KPI_StrikeRate" : "kpi_04_strike_rate.csv",
    "KPI_Boundary"   : "kpi_05_boundary_percentage.csv",
    "KPI_Economy"    : "kpi_06_economy_rate.csv",
    "KPI_DotBall"    : "kpi_07_dot_ball_percentage.csv",
    "KPI_Wickets"    : "kpi_08_wickets_per_bowler.csv",
    "KPI_Venue"      : "kpi_09_venue_win_percentage.csv",
    "KPI_BatVsChase" : "kpi_10_bat_vs_chase.csv",
    "KPI_BatChase_S" : "kpi_10_bat_vs_chase_season.csv",
}

kpi_data = {}
for sheet_name, filename in kpi_files.items():
    filepath = os.path.join(KPI_DIR, filename)
    if os.path.exists(filepath):
        kpi_data[sheet_name] = pd.read_csv(filepath)
        print(f"  ✔  {sheet_name:<20} → {kpi_data[sheet_name].shape[0]:>4} rows  |  {filename}")
    else:
        print(f"  ⚠️  MISSING: {filename} — run 02_kpi_engineering.py first!")

# ─────────────────────────────────────────────────────────
# 3. BUILD POWER BI MASTER TABLES
# ─────────────────────────────────────────────────────────
print("\n  [3/4] Building Power BI optimized tables...")

# ── 3A. DATE TABLE (for time intelligence in Power BI) ──
matches["date"] = pd.to_datetime(matches["date"], errors="coerce")
date_range = pd.date_range(
    start=matches["date"].min(),
    end  =matches["date"].max(),
    freq ="D"
)
date_table = pd.DataFrame({
    "date"        : date_range,
    "year"        : date_range.year,
    "month"       : date_range.month,
    "month_name"  : date_range.month_name(),
    "quarter"     : date_range.quarter,
    "day_of_week" : date_range.day_name(),
    "season"      : date_range.year,
})
print(f"  ✔  Date Table created  → {len(date_table):,} rows")

# ── 3B. TEAM DIMENSION TABLE ──
all_teams = pd.concat([
    matches["team1"].rename("team"),
    matches["team2"].rename("team")
]).drop_duplicates().dropna().sort_values().reset_index(drop=True)

team_table = pd.DataFrame({
    "team_id"  : range(1, len(all_teams) + 1),
    "team_name": all_teams.values
})
print(f"  ✔  Team Dimension      → {len(team_table)} teams")

# ── 3C. PLAYER DIMENSION TABLE ──
bat_col = "batter" if "batter" in deliveries.columns else "batsman"
batsmen = deliveries[bat_col].dropna().unique()
bowlers = deliveries["bowler"].dropna().unique()
all_players = pd.Series(list(set(batsmen) | set(bowlers))).sort_values().reset_index(drop=True)

player_table = pd.DataFrame({
    "player_id"  : range(1, len(all_players) + 1),
    "player_name": all_players.values,
    "is_batsman" : all_players.isin(batsmen).values,
    "is_bowler"  : all_players.isin(bowlers).values,
})
print(f"  ✔  Player Dimension    → {len(player_table):,} players")

# ── 3D. VENUE DIMENSION TABLE ──
venue_table = matches[["venue", "city"]].drop_duplicates().dropna(subset=["venue"]).sort_values("venue").reset_index(drop=True)
venue_table.insert(0, "venue_id", range(1, len(venue_table) + 1))
print(f"  ✔  Venue Dimension     → {len(venue_table)} venues")

# ── 3E. SEASON SUMMARY TABLE ──
valid_m = matches[matches["winner"] != "No Result"]
season_summary = matches.groupby("season").agg(
    total_matches     = ("match_id" if "match_id" in matches.columns else "id", "count"),
).reset_index()

season_runs = deliveries.groupby("season")["total_runs"].sum().reset_index(name="total_runs")
season_wkts = deliveries[deliveries["dismissal_kind"].notna()].groupby("season").size().reset_index(name="total_wickets")

season_summary = season_summary.merge(season_runs, on="season", how="left")
season_summary = season_summary.merge(season_wkts, on="season", how="left")
season_summary["avg_runs_per_match"] = (season_summary["total_runs"] / season_summary["total_matches"]).round(1)
print(f"  ✔  Season Summary      → {len(season_summary)} seasons")

# ── 3F. BATSMAN SEASON TABLE ──
bat_season = deliveries[deliveries["wide_runs"] == 0].groupby([bat_col, "season"]).agg(
    runs        = ("batsman_runs", "sum"),
    balls_faced = ("ball",         "count"),
    fours       = ("batsman_runs", lambda x: (x == 4).sum()),
    sixes       = ("batsman_runs", lambda x: (x == 6).sum()),
    matches     = ("match_id",     "nunique"),
).reset_index()
bat_season.rename(columns={bat_col: "batsman"}, inplace=True)
bat_season["strike_rate"] = ((bat_season["runs"] / bat_season["balls_faced"]) * 100).round(2)
print(f"  ✔  Batsman-Season      → {len(bat_season):,} rows")

# ── 3G. BOWLER SEASON TABLE ──
legal_d = deliveries[(deliveries["wide_runs"] == 0) & (deliveries["noball_runs"] == 0)]
BOWLER_WICKET_KINDS = ["caught", "bowled", "lbw", "stumped", "caught and bowled", "hit wicket"]

bowler_ball_season  = legal_d.groupby(["bowler", "season"])["ball"].count().reset_index(name="legal_balls")
bowler_run_season   = deliveries.groupby(["bowler", "season"])["total_runs"].sum().reset_index(name="runs_conceded")
bowler_wkt_season   = deliveries[deliveries["dismissal_kind"].isin(BOWLER_WICKET_KINDS)].groupby(
                          ["bowler", "season"]).size().reset_index(name="wickets")
bowler_dot_season   = legal_d[legal_d["total_runs"] == 0].groupby(
                          ["bowler", "season"]).size().reset_index(name="dot_balls")

bowler_season = bowler_ball_season \
    .merge(bowler_run_season,  on=["bowler", "season"], how="left") \
    .merge(bowler_wkt_season,  on=["bowler", "season"], how="left") \
    .merge(bowler_dot_season,  on=["bowler", "season"], how="left")

bowler_season["wickets"]           = bowler_season["wickets"].fillna(0).astype(int)
bowler_season["dot_balls"]         = bowler_season["dot_balls"].fillna(0).astype(int)
bowler_season["overs_bowled"]      = (bowler_season["legal_balls"] / 6).round(2)
bowler_season["economy_rate"]      = (bowler_season["runs_conceded"] / bowler_season["overs_bowled"]).round(2)
bowler_season["dot_ball_pct"]      = ((bowler_season["dot_balls"] / bowler_season["legal_balls"]) * 100).round(2)
print(f"  ✔  Bowler-Season       → {len(bowler_season):,} rows")

# ─────────────────────────────────────────────────────────
# 4. EXPORT TO EXCEL (MULTI-SHEET)
# ─────────────────────────────────────────────────────────
print("\n  [4/4] Writing to Excel workbook...")
print(f"  📂  Output: {OUTPUT_EXCEL}")

with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:

    # ── Core tables ──
    matches.to_excel(writer,        sheet_name="Matches",          index=False)
    date_table.to_excel(writer,     sheet_name="Date_Table",       index=False)
    team_table.to_excel(writer,     sheet_name="Dim_Teams",        index=False)
    player_table.to_excel(writer,   sheet_name="Dim_Players",      index=False)
    venue_table.to_excel(writer,    sheet_name="Dim_Venues",       index=False)
    season_summary.to_excel(writer, sheet_name="Season_Summary",   index=False)

    # ── Fact tables ──
    bat_season.to_excel(writer,     sheet_name="Fact_Batsman",     index=False)
    bowler_season.to_excel(writer,  sheet_name="Fact_Bowler",      index=False)

    # ── KPI tables ──
    for sheet_name, df in kpi_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("\n  ✅  Excel sheets written:")
print(f"  {'Sheet Name':<22} {'Rows':>6}")
print(f"  {'-'*30}")
print(f"  {'Matches':<22} {len(matches):>6,}")
print(f"  {'Date_Table':<22} {len(date_table):>6,}")
print(f"  {'Dim_Teams':<22} {len(team_table):>6}")
print(f"  {'Dim_Players':<22} {len(player_table):>6,}")
print(f"  {'Dim_Venues':<22} {len(venue_table):>6}")
print(f"  {'Season_Summary':<22} {len(season_summary):>6}")
print(f"  {'Fact_Batsman':<22} {len(bat_season):>6,}")
print(f"  {'Fact_Bowler':<22} {len(bowler_season):>6,}")
for sn, df in kpi_data.items():
    print(f"  {sn:<22} {len(df):>6,}")

print("\n" + "=" * 60)
print("  🎉 POWER BI EXPORT COMPLETE!")
print("  📌 Now open Power BI Desktop and import:")
print(f"     {OUTPUT_EXCEL}")
print("=" * 60)
