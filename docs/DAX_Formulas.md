# 📊 DAX Formulas Guide — IPL Power BI Dashboard

> **File:** `docs/DAX_Formulas.md`
> **Purpose:** All DAX measures and calculated columns used across the 4-page Power BI dashboard.
> Copy-paste these directly into Power BI Desktop → **Modeling → New Measure / New Column**

---

## 📁 Table of Contents

1. [Page 1 — Overall Tournament Insights](#page-1)
2. [Page 2 — Batsman Analysis](#page-2)
3. [Page 3 — Bowler Analysis](#page-3)
4. [Page 4 — Venue & Toss Analysis](#page-4)
5. [Time Intelligence Measures](#time-intelligence)
6. [Calculated Columns](#calculated-columns)
7. [How to Set Up Relationships](#relationships)

---

## ⚙️ Prerequisites — Relationships to Set in Power BI

Before using the measures, set these relationships in **Model View**:

| From Table | From Column | To Table | To Column | Cardinality |
|-----------|-------------|----------|-----------|-------------|
| `Fact_Batsman` | `season` | `Date_Table` | `season` | Many → One |
| `Fact_Bowler` | `season` | `Date_Table` | `season` | Many → One |
| `Matches` | `season` | `Date_Table` | `season` | Many → One |
| `KPI_BatsmanRuns` | `batsman` | `Dim_Players` | `player_name` | Many → One |
| `KPI_Wickets` | `bowler` | `Dim_Players` | `player_name` | Many → One |
| `KPI_Venue` | `venue` | `Dim_Venues` | `venue` | Many → One |

---

<a name="page-1"></a>
## 📄 Page 1 — Overall Tournament Insights

### 🔢 Card KPIs (use as Card visuals)

```dax
-- ① Total Matches Played
Total Matches = 
COUNTROWS( Matches )

-- ② Total Runs Scored
Total Runs = 
SUM( Fact_Batsman[runs] )

-- ③ Total Wickets Taken
Total Wickets = 
SUM( KPI_Wickets[wickets] )

-- ④ Total Seasons
Total Seasons = 
DISTINCTCOUNT( Matches[season] )

-- ⑤ Total Teams
Total Teams = 
COUNTROWS( Dim_Teams )

-- ⑥ Highest Score in a Season
Max Season Runs = 
MAXX(
    VALUES( Matches[season] ),
    CALCULATE( SUM( Fact_Batsman[runs] ) )
)
```

---

### 🏆 Win Percentage by Team (for Bar / Donut chart)

```dax
-- Total wins for selected team
Team Total Wins = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[winner] <> "No Result"
)

-- Team Win Percentage
Team Win % = 
DIVIDE(
    CALCULATE(
        COUNTROWS( Matches ),
        Matches[winner] = SELECTEDVALUE( Dim_Teams[team_name] )
    ),
    CALCULATE(
        COUNTROWS( Matches ),
        Matches[winner] <> "No Result"
    ),
    0
) * 100

-- Formatted Win % (for display)
Team Win % Label = 
FORMAT( [Team Win %], "0.00" ) & "%"
```

---

### 🎲 Toss Impact Measures

```dax
-- Toss Winner Also Won Match count
Toss Win & Match Win = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[toss_win_match_win] = 1,
    Matches[winner] <> "No Result"
)

-- Toss Impact Percentage
Toss Impact % = 
DIVIDE(
    [Toss Win & Match Win],
    CALCULATE(
        COUNTROWS( Matches ),
        Matches[winner] <> "No Result"
    ),
    0
) * 100

-- Bat win after toss
Toss + Bat Win = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[toss_decision] = "bat",
    Matches[toss_win_match_win] = 1,
    Matches[winner] <> "No Result"
)

-- Field win after toss
Toss + Field Win = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[toss_decision] = "field",
    Matches[toss_win_match_win] = 1,
    Matches[winner] <> "No Result"
)
```

---

### 📅 Season Filter Measure (for Slicer)

```dax
-- Selected Season label
Selected Season = 
IF(
    ISFILTERED( Date_Table[season] ),
    "Season: " & SELECTEDVALUE( Date_Table[season], "All" ),
    "All Seasons"
)
```

---

<a name="page-2"></a>
## 📄 Page 2 — Batsman Analysis

### 🏏 Top 10 Run Scorers

```dax
-- Total Runs (context-aware for player filter)
Batsman Total Runs = 
SUM( Fact_Batsman[runs] )

-- Balls Faced
Batsman Balls Faced = 
SUM( Fact_Batsman[balls_faced] )

-- Strike Rate
Batsman Strike Rate = 
DIVIDE(
    [Batsman Total Runs],
    [Batsman Balls Faced],
    0
) * 100

-- Formatted Strike Rate
Batsman SR Label = 
FORMAT( [Batsman Strike Rate], "0.00" )

-- Total Fours
Total Fours = 
SUM( Fact_Batsman[fours] )

-- Total Sixes
Total Sixes = 
SUM( Fact_Batsman[sixes] )

-- Boundary Runs
Boundary Runs = 
( [Total Fours] * 4 ) + ( [Total Sixes] * 6 )

-- Boundary Percentage
Boundary % = 
DIVIDE(
    [Total Fours] + [Total Sixes],
    [Batsman Balls Faced],
    0
) * 100

-- Average runs per match
Batting Average = 
DIVIDE(
    [Batsman Total Runs],
    DISTINCTCOUNT( Fact_Batsman[matches] ),
    0
)
```

---

### 📈 Runs by Season (for Line chart)

```dax
-- Season-wise runs for selected player
Runs This Season = 
CALCULATE(
    SUM( Fact_Batsman[runs] ),
    ALLEXCEPT( Fact_Batsman, Fact_Batsman[season], Fact_Batsman[batsman] )
)

-- Running Total Runs (cumulative)
Cumulative Runs = 
CALCULATE(
    SUM( Fact_Batsman[runs] ),
    FILTER(
        ALL( Date_Table[season] ),
        Date_Table[season] <= MAX( Date_Table[season] )
    )
)
```

---

### 🏅 Top N Batsman Filter (for dynamic Top N visual)

```dax
-- Rank batsmen by total runs (use in visual-level filter)
Batsman Rank by Runs = 
RANKX(
    ALL( Fact_Batsman[batsman] ),
    CALCULATE( SUM( Fact_Batsman[runs] ) ),
    ,
    DESC,
    DENSE
)

-- Top 10 flag (use as filter: Top10 Batsman = 1)
Top 10 Batsman = 
IF( [Batsman Rank by Runs] <= 10, 1, 0 )
```

---

<a name="page-3"></a>
## 📄 Page 3 — Bowler Analysis

### 🎾 Wicket Measures

```dax
-- Total Wickets (bowler context)
Bowler Total Wickets = 
SUM( Fact_Bowler[wickets] )

-- Overs Bowled
Bowler Overs = 
SUM( Fact_Bowler[overs_bowled] )

-- Runs Conceded
Bowler Runs Conceded = 
SUM( Fact_Bowler[runs_conceded] )

-- Economy Rate
Bowler Economy Rate = 
DIVIDE(
    [Bowler Runs Conceded],
    [Bowler Overs],
    0
)

-- Bowling Average
Bowling Average = 
DIVIDE(
    [Bowler Runs Conceded],
    [Bowler Total Wickets],
    0
)

-- Bowling Strike Rate (balls per wicket)
Bowling Strike Rate = 
DIVIDE(
    SUM( Fact_Bowler[legal_balls] ),
    [Bowler Total Wickets],
    0
)
```

---

### 🔵 Dot Ball Measures

```dax
-- Total Dot Balls
Total Dot Balls = 
SUM( Fact_Bowler[dot_balls] )

-- Total Legal Balls
Total Legal Balls = 
SUM( Fact_Bowler[legal_balls] )

-- Dot Ball Percentage
Dot Ball % = 
DIVIDE(
    [Total Dot Balls],
    [Total Legal Balls],
    0
) * 100

-- Formatted Dot Ball %
Dot Ball % Label = 
FORMAT( [Dot Ball %], "0.00" ) & "%"
```

---

### 🏅 Top N Bowler Rank

```dax
-- Rank bowlers by wickets
Bowler Rank by Wickets = 
RANKX(
    ALL( Fact_Bowler[bowler] ),
    CALCULATE( SUM( Fact_Bowler[wickets] ) ),
    ,
    DESC,
    DENSE
)

-- Top 10 flag
Top 10 Bowler = 
IF( [Bowler Rank by Wickets] <= 10, 1, 0 )

-- Wickets per Season (for line chart)
Wickets Per Season = 
CALCULATE(
    SUM( Fact_Bowler[wickets] ),
    ALLEXCEPT( Fact_Bowler, Fact_Bowler[season], Fact_Bowler[bowler] )
)
```

---

<a name="page-4"></a>
## 📄 Page 4 — Venue & Toss Analysis

### 🏟️ Venue Win Measures

```dax
-- Total matches at selected venue
Venue Total Matches = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[winner] <> "No Result"
)

-- Bat first wins at venue
Venue Bat First Wins = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[win_by_runs] > 0
)

-- Chase wins at venue
Venue Chase Wins = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[win_by_wickets] > 0
)

-- Bat First Win %
Venue Bat First Win % = 
DIVIDE(
    [Venue Bat First Wins],
    [Venue Total Matches],
    0
) * 100

-- Chase Win %
Venue Chase Win % = 
DIVIDE(
    [Venue Chase Wins],
    [Venue Total Matches],
    0
) * 100

-- Average runs per match at venue
Venue Avg Runs = 
DIVIDE(
    SUM( Fact_Batsman[runs] ),
    [Venue Total Matches],
    0
)
```

---

### 🎲 Toss Decision Trends

```dax
-- Times toss winner chose to Bat
Chose to Bat = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[toss_decision] = "bat"
)

-- Times toss winner chose to Field
Chose to Field = 
CALCULATE(
    COUNTROWS( Matches ),
    Matches[toss_decision] = "field"
)

-- Bat % after winning toss
Bat Decision % = 
DIVIDE(
    [Chose to Bat],
    COUNTROWS( Matches ),
    0
) * 100

-- Field % after winning toss
Field Decision % = 
DIVIDE(
    [Chose to Field],
    COUNTROWS( Matches ),
    0
) * 100

-- Season-wise toss decision trend label
Toss Trend Label = 
"Bat: " & FORMAT([Bat Decision %], "0.0") & "% | Field: " & FORMAT([Field Decision %], "0.0") & "%"
```

---

<a name="time-intelligence"></a>
## ⏱️ Time Intelligence Measures

```dax
-- Previous season runs (for YoY comparison)
Prev Season Runs = 
CALCULATE(
    SUM( Fact_Batsman[runs] ),
    PREVIOUSYEAR( Date_Table[date] )
)

-- YoY Run Change
YoY Run Change = 
[Batsman Total Runs] - [Prev Season Runs]

-- YoY % Change
YoY Run Change % = 
DIVIDE(
    [YoY Run Change],
    [Prev Season Runs],
    0
) * 100
```

---

<a name="calculated-columns"></a>
## 🧮 Calculated Columns

> Add these in **Table View → New Column**

```dax
-- In Matches table: Result Category
Result Category = 
SWITCH(
    TRUE(),
    Matches[win_by_runs] > 0,     "Bat First Win",
    Matches[win_by_wickets] > 0,  "Chase Win",
    Matches[winner] = "No Result","No Result",
    "Other"
)

-- In Matches table: Winning Margin Band
Margin Band = 
SWITCH(
    TRUE(),
    Matches[win_by_runs] >= 50,        "Dominant (50+ runs)",
    Matches[win_by_runs] >= 20,        "Comfortable (20-49 runs)",
    Matches[win_by_runs] > 0,          "Close (<20 runs)",
    Matches[win_by_wickets] >= 7,      "Dominant (7+ wkts)",
    Matches[win_by_wickets] >= 4,      "Comfortable (4-6 wkts)",
    Matches[win_by_wickets] > 0,       "Close (1-3 wkts)",
    "No Result"
)

-- In Fact_Batsman: Performance Category
Batsman Category = 
SWITCH(
    TRUE(),
    Fact_Batsman[runs] >= 1000, "Elite (1000+ runs)",
    Fact_Batsman[runs] >= 500,  "Top Performer (500+)",
    Fact_Batsman[runs] >= 200,  "Regular (200+)",
    "Lower Order"
)
```

---

<a name="relationships"></a>
## 🔗 Relationship Setup Checklist

```
Power BI Desktop → Model View

☐ Matches[season]        → Date_Table[season]       (Many:1, Active)
☐ Fact_Batsman[season]   → Date_Table[season]       (Many:1, Active)
☐ Fact_Bowler[season]    → Date_Table[season]       (Many:1, Active)
☐ KPI_Venue[venue]       → Dim_Venues[venue]        (Many:1, Active)
☐ Fact_Batsman[batsman]  → Dim_Players[player_name] (Many:1, Active)
☐ Fact_Bowler[bowler]    → Dim_Players[player_name] (Many:1, Inactive*)

* Use USERELATIONSHIP() in DAX for inactive relationships
```

---

## 💡 Pro Tips for Power BI

| Tip | Details |
|-----|---------|
| **Mark Date Table** | Right-click `Date_Table` → Mark as Date Table → Select `date` column |
| **Format Numbers** | Set measure format to `0.00` for percentages, `#,##0` for counts |
| **Cross-filter** | Set cross-filter direction to **Both** for Player ↔ Matches |
| **Visual Interactions** | Use Format → Edit Interactions to control which visuals filter each other |
| **Bookmarks** | Create bookmarks for "All Seasons" vs specific season views |
| **Tooltips** | Add Economy Rate and Dot Ball % as tooltip page for bowler visuals |

---

*Generated for IPL Performance Analytics Project — February 2026*
