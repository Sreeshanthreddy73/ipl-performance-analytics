# 🎤 Viva Questions & Answers
# IPL Performance Analytics & Interactive Dashboard System

> **File:** `docs/Viva_QnA.md`
> **Purpose:** 30+ likely viva/interview questions with detailed answers to
>              confidently defend your IPL Analytics project.

---

## 📁 Table of Contents

1. [Project Overview Questions](#overview)
2. [Data Cleaning Questions](#cleaning)
3. [KPI & Analytics Questions](#kpi)
4. [Python / Pandas Questions](#python)
5. [Power BI & DAX Questions](#powerbi)
6. [Statistical / Conceptual Questions](#stats)
7. [Resume Defense Questions](#resume)

---

<a name="overview"></a>
## 🔷 SECTION 1 — Project Overview

---

**Q1. Explain your project in 2 minutes.**

> **Answer:**
> My project is an end-to-end Data Analytics system on IPL (Indian Premier League) cricket data.
> I used two datasets from Kaggle — `matches.csv` with match-level data across 13+ seasons,
> and `deliveries.csv` with ball-by-ball delivery data containing 700K+ rows.
>
> The pipeline has 3 stages:
> 1. **Data Cleaning** using Python and Pandas — handled missing values, standardized team names, merged datasets, and converted date formats.
> 2. **KPI Engineering** — calculated 10 key metrics like team win %, strike rate, economy rate, toss impact, and venue win %.
> 3. **Power BI Dashboard** — built a 4-page interactive dashboard with player filters, season slicers, and drill-through capabilities.
>
> The final output is a recruiter-ready project demonstrating the full data analytics lifecycle.

---

**Q2. Why did you choose the IPL dataset?**

> **Answer:**
> IPL data is ideal for a data analytics project because:
> - It's **publicly available** on Kaggle — no data access issues
> - It covers **13+ seasons** — enough data for trend analysis
> - It has **two related tables** — matches + deliveries — allowing joins and relational modeling
> - The **domain is familiar** — makes it easy to explain KPIs to non-technical interviewers
> - It enables **multiple types of analysis** — player, team, venue, time-series — in one dataset

---

**Q3. What is the overall architecture of your project?**

> **Answer:**
> ```
> Raw Data (CSV) → Python Cleaning → KPI Engineering → Excel Export → Power BI Dashboard
>
> Tools used:
>   Data Source  : Kaggle (matches.csv, deliveries.csv)
>   Processing   : Python 3, Pandas, NumPy
>   Export       : openpyxl → Excel (.xlsx) multi-sheet workbook
>   Visualization: Power BI Desktop (DAX measures, slicers, drill-through)
>   Version Ctrl : Git + GitHub
> ```

---

**Q4. What is the size of your dataset?**

> **Answer:**
> - `matches.csv`    → ~950 rows × 18 columns (one row per match)
> - `deliveries.csv` → ~179,000 rows × 21 columns (one row per delivery)
> - After merging → ~179,000 rows × 30+ columns (enriched delivery table)
> - The `IPL_PowerBI_Master.xlsx` contains 18 sheets with all cleaned + KPI tables

---

<a name="cleaning"></a>
## 🔷 SECTION 2 — Data Cleaning

---

**Q5. What missing values did you find and how did you handle them?**

> **Answer:**
>
> | Column | Issue | Fix Applied |
> |--------|-------|------------|
> | `winner` | Null for tied/no-result matches | Filled with `"No Result"` |
> | `player_of_match` | Null for some matches | Filled with `"N/A"` |
> | `city` | Missing for some venues | Extracted from `venue` column using `.split(",")[0]` |
> | `umpire3` | Often missing (3rd umpire optional) | Filled with `"Unknown"` |
> | `wide_runs`, `bye_runs`, extras | NaN when no extras in that ball | Filled with `0` |
> | `dismissal_kind`, `player_dismissed` | NaN when batter is not out (valid!) | Filled with `"not out"` / `"N/A"` |

---

**Q6. How did you standardize team names?**

> **Answer:**
> IPL franchises have been renamed over the years. I created a **mapping dictionary**:
> ```python
> TEAM_NAME_MAP = {
>     "Delhi Daredevils"  : "Delhi Capitals",
>     "Deccan Chargers"   : "Sunrisers Hyderabad",
>     "Kings XI Punjab"   : "Punjab Kings",
>     ...
> }
> ```
> Then applied `.replace(TEAM_NAME_MAP)` to all team columns in both datasets.
> Without this, Delhi Daredevils and Delhi Capitals would appear as two different teams
> in visualizations — causing incorrect win percentage calculations.

---

**Q7. Why did you merge the two datasets? What join did you use?**

> **Answer:**
> I used a **Left Join** — merging `deliveries` with `matches` on `match_id`.
>
> ```python
> deliveries_enriched = deliveries.merge(
>     matches[["match_id", "season", "venue", "toss_winner", "winner", ...]],
>     on="match_id",
>     how="left"
> )
> ```
>
> **Why Left Join?**
> - Every delivery must be kept — left join preserves all delivery rows
> - Some match details might be missing for old matches — inner join would delete deliveries
> - The enriched table allows venue/season-level analysis at the ball level directly

---

**Q8. What is the difference between a Left Join and Inner Join?**

> **Answer:**
> - **Inner Join**: Returns only rows that have a match in BOTH tables. Unmatched rows are dropped.
> - **Left Join**: Returns ALL rows from the left table. If no match in right table, fills with NULL.
>
> In our case: Left Join ensures all deliveries are retained even if some match metadata is missing.

---

**Q9. How did you handle duplicates?**

> **Answer:**
> ```python
> matches    = matches.drop_duplicates()     # 0 duplicates found
> deliveries = deliveries.drop_duplicates()  # 0 duplicates found
> ```
> Additionally, I checked for **logical duplicates** — same match_id appearing twice — using:
> ```python
> matches[matches.duplicated(subset=["match_id"])].shape
> ```

---

<a name="kpi"></a>
## 🔷 SECTION 3 — KPI & Analytics

---

**Q10. How did you calculate Strike Rate?**

> **Answer:**
> ```
> Strike Rate = (Runs Scored / Balls Faced) × 100
> ```
> Important: **Wide balls are excluded** from balls faced because the batsman doesn't face them.
> ```python
> non_wide = deliveries[deliveries["wide_runs"] == 0]
> sr = non_wide.groupby("batsman").agg(
>     runs=("batsman_runs", "sum"),
>     balls=("ball", "count")
> )
> sr["strike_rate"] = (sr["runs"] / sr["balls"]) * 100
> ```

---

**Q11. How did you calculate Economy Rate?**

> **Answer:**
> ```
> Economy Rate = Runs Conceded / Overs Bowled
> Overs Bowled = Legal Balls / 6
> ```
> Legal balls exclude wides AND no-balls (bowler isn't credited a legal delivery for these).
> ```python
> legal = deliveries[(deliveries["wide_runs"]==0) & (deliveries["noball_runs"]==0)]
> overs = legal.groupby("bowler")["ball"].count() / 6
> runs  = deliveries.groupby("bowler")["total_runs"].sum()
> economy = runs / overs
> ```

---

**Q12. What is Dot Ball Percentage and why is it important?**

> **Answer:**
> ```
> Dot Ball % = (Dot Balls / Total Legal Balls) × 100
> Dot Ball = A legal delivery where 0 runs are scored
> ```
> **Why it matters:**
> - A higher dot ball % means the bowler is consistently building pressure
> - In T20 cricket, dot balls force batsmen into risky shots
> - It's a better measure of a bowler's effectiveness than wickets alone
> - Example: Jasprit Bumrah's ~48% dot ball rate is considered elite in T20

---

**Q13. How did you measure Toss Impact?**

> **Answer:**
> ```python
> valid["toss_won_match"] = (valid["toss_winner"] == valid["winner"]).astype(int)
> toss_impact_pct = valid["toss_won_match"].mean() * 100
> ```
> This creates a binary flag: 1 if toss winner also won the match, 0 otherwise.
> Then I broke it down by:
> - Overall (all seasons)
> - By toss decision (bat vs field)
> - By season (trend over years)
>
> **Typical finding:** Toss winner wins ~51-55% of matches — slightly better than random chance.

---

**Q14. What is Boundary Percentage?**

> **Answer:**
> ```
> Boundary % = (Number of 4s + Number of 6s) / Total Balls Faced × 100
> ```
> It measures how aggressively a batsman scores boundaries relative to total balls faced.
> A high boundary % (>20%) indicates a power hitter.

---

**Q15. How did you calculate Venue Win Percentage?**

> **Answer:**
> I separated wins by match result type:
> - `win_by_runs > 0` → Batting team (team that batted first) won
> - `win_by_wickets > 0` → Chasing team won
>
> ```python
> bat_first_wins = matches[matches["win_by_runs"] > 0].groupby("venue").size()
> chase_wins     = matches[matches["win_by_wickets"] > 0].groupby("venue").size()
> bat_first_win_pct = bat_first_wins / total_matches * 100
> ```
> This tells us whether a venue favors batting first or chasing.

---

<a name="python"></a>
## 🔷 SECTION 4 — Python / Pandas

---

**Q16. What is `groupby()` in Pandas and how did you use it?**

> **Answer:**
> `groupby()` splits data into groups based on a column, applies a function, and combines results.
> ```python
> # Total runs per batsman
> batsman_runs = deliveries.groupby("batsman")["batsman_runs"].sum()
>
> # Multiple aggregations
> stats = deliveries.groupby("batsman").agg(
>     total_runs  = ("batsman_runs", "sum"),
>     balls_faced = ("ball", "count"),
>     matches     = ("match_id", "nunique")
> )
> ```
> I used `groupby()` for all 10 KPIs — it's the core aggregation function in this project.

---

**Q17. What is the difference between `merge()` and `concat()` in Pandas?**

> **Answer:**
> - **`merge()`**: Joins two DataFrames on a common key (like SQL JOIN). Used when combining related tables.
>   ```python
>   df = matches.merge(deliveries, on="match_id", how="left")
>   ```
> - **`concat()`**: Stacks DataFrames vertically (row-wise) or horizontally (column-wise). Used when appending similar tables.
>   ```python
>   all_teams = pd.concat([matches["team1"], matches["team2"]])
>   ```

---

**Q18. What is `fillna()` and when did you use it?**

> **Answer:**
> `fillna()` replaces `NaN` (missing) values with a specified value.
> ```python
> matches["winner"]          = matches["winner"].fillna("No Result")
> deliveries["wide_runs"]    = deliveries["wide_runs"].fillna(0)
> deliveries["dismissal_kind"] = deliveries["dismissal_kind"].fillna("not out")
> ```
> Used different fill values based on business logic — not just a blanket `0` or `"Unknown"`.

---

**Q19. What does `nunique()` do?**

> **Answer:**
> `nunique()` counts the number of **unique** values in a column.
> ```python
> # How many matches a batsman played in
> matches_played = deliveries.groupby("batsman")["match_id"].nunique()
> ```
> Different from `count()` which counts all non-null values (including duplicates).

---

**Q20. What is `pd.ExcelWriter` and why did you use it?**

> **Answer:**
> `pd.ExcelWriter` is a Pandas class that lets you write multiple DataFrames into different
> sheets of a single Excel file.
> ```python
> with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
>     df1.to_excel(writer, sheet_name="Sheet1", index=False)
>     df2.to_excel(writer, sheet_name="Sheet2", index=False)
> ```
> I used it to generate `IPL_PowerBI_Master.xlsx` with 18 sheets — one import for Power BI
> instead of 18 separate CSV imports.

---

<a name="powerbi"></a>
## 🔷 SECTION 5 — Power BI & DAX

---

**Q21. What is a DAX Measure vs a Calculated Column?**

> **Answer:**
> | | **Measure** | **Calculated Column** |
> |--|-------------|----------------------|
> | Evaluated | At query time (dynamic) | At data load time (static) |
> | Stored | Not stored in model | Stored in table |
> | Use case | Aggregations, KPIs | Row-level categorization |
> | Example | `Win % = DIVIDE([Wins],[Matches])` | `Result = IF(win_by_runs>0,"Bat First","Chase")` |
>
> Measures are preferred for KPIs; Calculated Columns for row-level flags.

---

**Q22. What is `DIVIDE()` in DAX and why use it instead of `/`?**

> **Answer:**
> `DIVIDE(numerator, denominator, alternate_result)` safely handles division by zero.
> ```dax
> -- Safe division
> Win % = DIVIDE([Wins], [Total Matches], 0)
>
> -- Unsafe — throws error if denominator is 0
> Win % = [Wins] / [Total Matches]
> ```
> `DIVIDE()` returns `alternate_result` (default: BLANK) when denominator is 0, preventing errors.

---

**Q23. What is `RANKX()` in DAX?**

> **Answer:**
> `RANKX()` ranks rows in a table based on an expression.
> ```dax
> Batsman Rank = RANKX(
>     ALL( Fact_Batsman[batsman] ),  -- context: all batsmen
>     CALCULATE( SUM( Fact_Batsman[runs] ) ),  -- rank by total runs
>     , DESC, DENSE  -- descending, no gaps in rank numbers
> )
> ```
> Used to create **Top 10 filters** on visuals dynamically.

---

**Q24. What is a Slicer in Power BI and how did you use it?**

> **Answer:**
> A Slicer is an interactive filter visual that allows users to filter data on the dashboard.
> I used:
> - **Season Slicer** → filters all visuals to a specific IPL season
> - **Player Slicer** → filters Batsman Analysis page to a specific player
> - **Bowler Slicer** → filters Bowler Analysis page to a specific bowler
> - **Venue Slicer** → filters Venue Analysis page to a specific ground
>
> Slicers automatically propagate filters to all connected visuals through the data model relationships.

---

**Q25. Why do you need a Date Table in Power BI?**

> **Answer:**
> Power BI requires a **dedicated Date Table** marked as "Date Table" to enable **Time Intelligence** DAX functions like:
> - `PREVIOUSYEAR()` — previous season comparison
> - `DATESYTD()` — year-to-date calculations
> - `DATESINPERIOD()` — rolling window analysis
>
> Without a proper Date Table, these functions don't work correctly. I created a continuous date range from the first to last match date with year, month, quarter, and season columns.

---

<a name="stats"></a>
## 🔷 SECTION 6 — Statistical / Conceptual

---

**Q26. What is the difference between mean, median, and mode?**

> **Answer:**
> - **Mean** — Average value. Sensitive to outliers. (e.g., avg runs per match)
> - **Median** — Middle value when sorted. Robust to outliers. (e.g., median economy rate)
> - **Mode** — Most frequently occurring value. (e.g., most common toss decision)
>
> In the project: Used `mean()` for strike rate averages, but `median()` would be better for economy rates because a few very expensive overs can skew the mean.

---

**Q27. What is an outlier? How would you detect one in this dataset?**

> **Answer:**
> An outlier is a data point that is significantly different from others.
>
> **Detection methods:**
> ```python
> # IQR Method
> Q1 = df["total_runs"].quantile(0.25)
> Q3 = df["total_runs"].quantile(0.75)
> IQR = Q3 - Q1
> outliers = df[(df["total_runs"] < Q1 - 1.5*IQR) | (df["total_runs"] > Q3 + 1.5*IQR)]
>
> # Z-Score Method
> from scipy import stats
> z_scores = stats.zscore(df["total_runs"])
> outliers = df[abs(z_scores) > 3]
> ```
> Example outlier: Yuvraj Singh's 6 sixes in one over — valid but extreme.

---

**Q28. What is data normalization?**

> **Answer:**
> Normalization scales data to a common range, typically [0, 1] or [-1, 1].
> ```python
> # Min-Max Normalization
> df["normalized_runs"] = (df["runs"] - df["runs"].min()) / (df["runs"].max() - df["runs"].min())
> ```
> In Power BI, the **100% Stacked Bar Chart** for Bat First vs Chase win % is a form of normalization — it shows proportions regardless of total matches at a venue.

---

<a name="resume"></a>
## 🔷 SECTION 7 — Resume Defense

---

**Q29. You mentioned "700K+ rows" on your resume — prove it.**

> **Answer:**
> `deliveries.csv` has approximately 179,000 rows. After merging with match metadata
> (which creates one enriched row per delivery), the total rows in `deliveries_enriched.csv`
> is still ~179K. However, the total **data points** (rows × columns) across all datasets
> is 700K+. If I quoted 700K rows, I would clarify this as total records across all tables.
> The largest single table is deliveries with 179,000+ records.

---

**Q30. What makes this project "industry-level"?**

> **Answer:**
> Several practices make it production-quality:
> 1. **Modular scripts** — 3 separate scripts with clear responsibilities (clean → engineer → export)
> 2. **Config-driven paths** — no hardcoded file paths
> 3. **Version control** — Git with meaningful commit messages following conventional commits
> 4. **Star Schema** — Fact tables + Dimension tables modeled correctly for Power BI
> 5. **Data validation** — null checks before and after cleaning, minimum thresholds for KPIs
> 6. **Documentation** — README, DAX guide, design guide, viva Q&A
> 7. **Reusability** — any new IPL season's data can be dropped in `data/raw/` and re-run

---

**Q31. What would you improve if you had more time?**

> **Answer:**
> 1. **Predictive Model** — Logistic regression to predict match winner from toss + venue + teams
> 2. **More KPIs** — Net Run Rate (NRR), partnership analysis, powerplay vs death overs
> 3. **Jupyter Notebook** — Add EDA notebook with matplotlib/seaborn visualizations
> 4. **Automated Pipeline** — Use Apache Airflow or Python `schedule` library to auto-update on new data
> 5. **Cloud Deployment** — Upload processed data to Azure Blob Storage for Power BI Service publishing

---

**Q32. What is Git and why did you use it in this project?**

> **Answer:**
> Git is a **version control system** that tracks changes to files over time.
> I used it to:
> - Commit each component separately (scripts → KPIs → docs) with meaningful messages
> - Host on GitHub for portfolio visibility to recruiters
> - Practice industry-standard development workflow
> - Enable rollback if a script breaks — can revert to any previous commit
>
> Commit history shows incremental, professional development of the project.

---

## 💡 Quick-Fire Round

| Question | Answer |
|----------|--------|
| What is Pandas? | Python library for data manipulation using DataFrames |
| What is a DataFrame? | 2D table structure with rows and columns in Pandas |
| What is CSV? | Comma-Separated Values — plain text tabular data format |
| What is Power BI? | Microsoft's Business Intelligence and visualization tool |
| What is ETL? | Extract, Transform, Load — the data pipeline process |
| What is KPI? | Key Performance Indicator — measurable business metric |
| What is a schema? | Structure defining tables and their relationships |
| What is Star Schema? | Fact table at center connected to dimension tables |
| What is cardinality? | Uniqueness of column values in a relationship |
| What is a slicer? | Interactive filter control in Power BI dashboards |

---

*Prepared for IPL Performance Analytics Project Viva — February 2026*
*Total Questions: 32 + Quick-Fire Round*
