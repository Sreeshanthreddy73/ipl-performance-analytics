# 🎨 Power BI Dashboard Design Guide
# IPL Performance Analytics & Interactive Dashboard System

> **File:** `docs/Dashboard_Design.md`
> **Purpose:** Exact layout, visual types, colors, fonts, slicers, and placement
>              instructions for all 4 pages of the Power BI dashboard.

---

## 📐 Canvas Settings (Apply to ALL Pages)

```
File → Options → Report Settings
  Canvas Size   : 16:9  (1280 × 720 px)  ← Standard widescreen
  Background    : Custom Color  #0D1117   (Dark Navy — premium look)
  Wallpaper     : None
```

---

## 🎨 Global Theme & Color Palette

### Primary Colors
| Role | Hex Code | Use |
|------|----------|-----|
| Background | `#0D1117` | Page background |
| Card Background | `#161B22` | All card/visual backgrounds |
| Accent Blue | `#1F6FEB` | Primary highlights, headers |
| Accent Orange | `#F78166` | IPL brand feel, key metrics |
| Accent Gold | `#E3B341` | Awards, rankings, top performers |
| Success Green | `#3FB950` | Positive trends, wins |
| Muted White | `#E6EDF3` | Primary text |
| Subtle Grey | `#8B949E` | Secondary text, grid lines |

### Team Color Coding (for team visuals)
| Team | Color |
|------|-------|
| Mumbai Indians | `#004BA0` |
| Chennai Super Kings | `#FDB913` |
| Royal Challengers Bangalore | `#EC1C24` |
| Kolkata Knight Riders | `#3A225D` |
| Delhi Capitals | `#00008B` |
| Sunrisers Hyderabad | `#F7A721` |
| Rajasthan Royals | `#EA1A85` |
| Punjab Kings | `#ED1B24` |

### Font Settings
```
Title Font      : Segoe UI Semibold,  Size 16,  Color #E6EDF3
Subtitle Font   : Segoe UI,           Size 11,  Color #8B949E
Data Label Font : Segoe UI,           Size 10,  Color #E6EDF3
Axis Font       : Segoe UI,           Size 9,   Color #8B949E
```

---

## 🏠 Navigation Bar (All Pages — Top Strip)

```
┌────────────────────────────────────────────────────────────────────┐
│  🏏 IPL Analytics    [Page1]  [Page2]  [Page3]  [Page4]           │
└────────────────────────────────────────────────────────────────────┘

Implementation:
  - Insert a Rectangle shape: W=1280px, H=50px, Y=0
  - Fill: #161B22  |  Border: None
  - Add Text Box: "🏏 IPL Performance Analytics" → Font: Segoe UI Bold, 14pt
  - Add 4 Buttons (one per page) → Action = Page Navigation
  - Button Style: Fill=#1F6FEB (active), Fill=#8B949E (inactive)
  - Place all buttons in group for easy management
```

---

## ═══════════════════════════════════════
## 📄 PAGE 1 — Overall Tournament Insights
## ═══════════════════════════════════════

### Page Layout (1280 × 720)

```
┌──────────────────────────────────────────────────────────────────┐
│  NAV BAR                                              [Slicer]   │
├──────────────────────────────────────────────────────────────────│
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  TOTAL   │  │  TOTAL   │  │  TOTAL   │  │  TOTAL   │        │
│  │ MATCHES  │  │   RUNS   │  │ WICKETS  │  │ SEASONS  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                                                  │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐ │
│  │  Win % by Team          │  │  Toss Impact                  │ │
│  │  (Horizontal Bar Chart) │  │  (Donut Chart)                │ │
│  │                         │  │                               │ │
│  └─────────────────────────┘  └───────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Matches per Season  (Column Chart)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### Visual Specifications

#### 🃏 KPI Cards (Row 1 — 4 Cards)
| Card | Measure | Position |
|------|---------|----------|
| Total Matches | `Total Matches` | X:60, Y:70, W:250, H:100 |
| Total Runs | `Total Runs` | X:340, Y:70, W:250, H:100 |
| Total Wickets | `Total Wickets` | X:620, Y:70, W:250, H:100 |
| Total Seasons | `Total Seasons` | X:900, Y:70, W:250, H:100 |

```
Card Formatting:
  Background     : #161B22
  Border Radius  : 8px
  Border Color   : #1F6FEB  (1px)
  Title          : ON  (subtitle text)
  Value Font     : 28pt, Bold, #F78166
  Label Font     : 11pt, #8B949E
  Callout Value  : ON
```

#### 📊 Win % by Team — Horizontal Bar Chart
```
Visual Type    : Clustered Bar Chart
Data:
  Y-Axis       : Dim_Teams[team_name]
  X-Axis       : [Team Win %]
  Tooltips     : [Team Total Wins], [Team Win % Label]

Position       : X:60, Y:200, W:580, H:220

Formatting:
  Bar Color    : Conditional (top 3 = #E3B341, rest = #1F6FEB)
  Background   : #161B22
  Grid Lines   : #8B949E  (subtle, 0.5pt)
  Data Labels  : ON, Font=10pt, Color=#E6EDF3
  Sort         : Descending by [Team Win %]
  Title        : "Team Win Percentage"  |  Font=14pt, Color=#E6EDF3
```

#### 🍩 Toss Impact — Donut Chart
```
Visual Type    : Donut Chart
Data:
  Legend       : KPI_TossImpact[metric]
  Values       : KPI_TossImpact[count]
  Tooltips     : KPI_TossImpact[percentage]

Position       : X:680, Y:200, W:540, H:220

Formatting:
  Inner Label  : "Toss Impact"
  Color 1      : #3FB950  (Won Match)
  Color 2      : #F78166  (Lost Match)
  Legend       : Bottom, Font=10pt, Color=#E6EDF3
  Background   : #161B22
  Border       : None
  Title        : "Toss Impact on Match Result"
```

#### 📈 Matches per Season — Column Chart
```
Visual Type    : Clustered Column Chart
Data:
  X-Axis       : Matches[season]
  Y-Axis       : [Total Matches]
  Tooltips     : [Total Runs], [Total Wickets]

Position       : X:60, Y:450, W:1160, H:220

Formatting:
  Column Color : Gradient (#1F6FEB → #3FB950)
  Data Labels  : ON, Position=Outside End
  Background   : #161B22
  X-Axis       : Rotate 0°, Font=9pt
  Title        : "Matches per Season"
  Reference Line: Average line, Color=#E3B341, Label=ON
```

#### 🔽 Season Slicer
```
Visual Type    : Slicer
Field          : Date_Table[season]
Style          : Dropdown
Position       : X:1080, Y:58, W:170, H:36

Formatting:
  Background   : #161B22
  Border       : #1F6FEB
  Font         : 10pt, #E6EDF3
  Header       : "Filter by Season"
```

---

## ════════════════════════════
## 📄 PAGE 2 — Batsman Analysis
## ════════════════════════════

### Page Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  NAV BAR                          [Player Slicer] [Season Slicer]│
├──────────────────────────────────────────────────────────────────│
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  TOTAL   │  │  STRIKE  │  │  FOURS   │  │  SIXES   │        │
│  │   RUNS   │  │   RATE   │  │          │  │          │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                                                  │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐ │
│  │  Top 10 Run Scorers     │  │  Runs by Season (Line Chart)  │ │
│  │  (Horizontal Bar Chart) │  │                               │ │
│  └─────────────────────────┘  └───────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐ │
│  │  Strike Rate Comparison │  │  Boundary % Scatter Plot      │ │
│  │  (Bar + Line Combo)     │  │  (Scatter Chart)              │ │
│  └─────────────────────────┘  └───────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### Visual Specifications

#### 🃏 KPI Cards (Row 1)
| Card | Measure |
|------|---------|
| Total Runs | `Batsman Total Runs` → Value Color: `#F78166` |
| Strike Rate | `Batsman Strike Rate` → Value Color: `#E3B341` |
| Total Fours | `Total Fours` → Value Color: `#3FB950` |
| Total Sixes | `Total Sixes` → Value Color: `#1F6FEB` |

#### 📊 Top 10 Run Scorers — Horizontal Bar Chart
```
Visual Type    : Clustered Bar Chart
Data:
  Y-Axis       : Fact_Batsman[batsman]
  X-Axis       : [Batsman Total Runs]
  Filter       : [Top 10 Batsman] = 1

Position       : X:60, Y:200, W:540, H:220

Formatting:
  Bar Color    : #F78166 (orange — batsman theme)
  Top Bar      : #E3B341 (gold — for #1 rank)
  Sort         : Desc by [Batsman Total Runs]
  Data Labels  : ON
  Title        : "Top 10 Run Scorers (All Time)"
```

#### 📈 Runs by Season — Line Chart
```
Visual Type    : Line Chart
Data:
  X-Axis       : Fact_Batsman[season]
  Y-Axis       : [Batsman Total Runs]
  Legend       : Fact_Batsman[batsman]  (active only when player selected)

Position       : X:640, Y:200, W:580, H:220

Formatting:
  Line Color   : #F78166
  Line Width   : 2.5pt
  Markers      : ON (circle, size 5)
  Data Labels  : ON for endpoints only
  Shaded Area  : ON (transparency 80%)
  Title        : "Runs by Season"
```

#### 📊 Strike Rate Comparison — Bar + Line Combo
```
Visual Type    : Line and Clustered Column Chart
Data:
  X-Axis       : Fact_Batsman[batsman]
  Column Y     : [Batsman Total Runs]
  Line Y       : [Batsman Strike Rate]
  Filter       : [Top 10 Batsman] = 1

Position       : X:60, Y:450, W:540, H:230

Formatting:
  Column Color : #1F6FEB
  Line Color   : #E3B341
  Secondary Axis: ON (for Strike Rate)
  Title        : "Runs vs Strike Rate — Top 10"
```

#### 🔵 Boundary % Scatter Plot
```
Visual Type    : Scatter Chart
Data:
  X-Axis       : [Batsman Total Runs]
  Y-Axis       : [Boundary %]
  Size         : [Batsman Balls Faced]
  Legend       : Fact_Batsman[batsman]
  Filter       : balls_faced >= 200

Position       : X:640, Y:450, W:580, H:230

Formatting:
  Bubble Color : Conditional — Boundary% > 20 = #E3B341, else #1F6FEB
  Crosshair    : ON
  Zoom Slider  : ON
  Title        : "Boundary % vs Total Runs"
```

#### 🔽 Player Slicer
```
Visual Type    : Slicer
Field          : Dim_Players[player_name]
Style          : Dropdown  (search enabled)
Position       : X:800, Y:58, W:220, H:36
```

---

## ══════════════════════════
## 📄 PAGE 3 — Bowler Analysis
## ══════════════════════════

### Page Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  NAV BAR                          [Bowler Slicer] [Season Slicer]│
├──────────────────────────────────────────────────────────────────│
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  TOTAL   │  │  ECONOMY │  │  DOT     │  │ BOWLING  │        │
│  │ WICKETS  │  │   RATE   │  │  BALL %  │  │   AVG    │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                                                  │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐ │
│  │  Top 10 Wicket Takers   │  │  Economy Rate Comparison      │ │
│  │  (Horizontal Bar)       │  │  (Bar Chart, sorted ASC)      │ │
│  └─────────────────────────┘  └───────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐ │
│  │  Wickets per Season     │  │  Dot Ball % Comparison        │ │
│  │  (Area Chart)           │  │  (Horizontal Bar)             │ │
│  └─────────────────────────┘  └───────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### Visual Specifications

#### 🃏 KPI Cards (Row 1)
| Card | Measure | Color |
|------|---------|-------|
| Total Wickets | `Bowler Total Wickets` | `#3FB950` |
| Economy Rate | `Bowler Economy Rate` | `#E3B341` |
| Dot Ball % | `Dot Ball %` | `#1F6FEB` |
| Bowling Average | `Bowling Average` | `#F78166` |

#### 📊 Top 10 Wicket Takers — Horizontal Bar
```
Visual Type    : Clustered Bar Chart
Data:
  Y-Axis       : Fact_Bowler[bowler]
  X-Axis       : [Bowler Total Wickets]
  Tooltip      : [Bowling Average], [Bowler Economy Rate]
  Filter       : [Top 10 Bowler] = 1

Formatting:
  Bar Color    : #3FB950 (green — bowler theme)
  Top Bar      : #E3B341
  Sort         : Desc by wickets
  Data Labels  : ON
  Title        : "Top 10 Wicket Takers (All Time)"
```

#### 📊 Economy Rate Comparison — Bar Chart
```
Visual Type    : Clustered Bar Chart
Data:
  Y-Axis       : Fact_Bowler[bowler]
  X-Axis       : [Bowler Economy Rate]
  Filter       : overs_bowled >= 10, [Top 10 Bowler] = 1

Formatting:
  Bar Color    : Conditional — Economy < 7 = #3FB950, else #F78166
  Sort         : ASC (lower economy = better)
  Title        : "Economy Rate — Top 10 Bowlers"
  Reference Line: 8.0 (benchmark), Color=#E3B341
```

#### 📈 Wickets per Season — Area Chart
```
Visual Type    : Area Chart
Data:
  X-Axis       : Fact_Bowler[season]
  Y-Axis       : [Bowler Total Wickets]
  Legend       : Fact_Bowler[bowler]  (when bowler selected)

Formatting:
  Area Fill    : #3FB950  (opacity 40%)
  Line Color   : #3FB950  (solid)
  Line Width   : 2pt
  Markers      : ON
  Title        : "Wickets by Season"
```

#### 📊 Dot Ball % Comparison — Horizontal Bar
```
Visual Type    : Clustered Bar Chart
Data:
  Y-Axis       : Fact_Bowler[bowler]
  X-Axis       : [Dot Ball %]
  Filter       : legal_balls >= 60, [Top 10 Bowler] = 1

Formatting:
  Bar Color    : #1F6FEB
  Sort         : DESC
  Data Labels  : ON (format "0.0%")
  Title        : "Dot Ball % — Top 10 Bowlers"
```

---

## ════════════════════════════════════
## 📄 PAGE 4 — Venue & Toss Analysis
## ════════════════════════════════════

### Page Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  NAV BAR                              [Venue Slicer]             │
├──────────────────────────────────────────────────────────────────│
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  VENUES  │  │ BAT 1ST  │  │  CHASE   │  │   AVG    │        │
│  │  TOTAL   │  │  WIN %   │  │  WIN %   │  │  RUNS    │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                                                  │
│  ┌─────────────────────────────────────────┐  ┌──────────────┐  │
│  │  Venue Win %: Bat 1st vs Chase          │  │ Toss         │  │
│  │  (Stacked Bar — 100% normalized)        │  │ Decision     │  │
│  │                                         │  │ Donut Chart  │  │
│  └─────────────────────────────────────────┘  └──────────────┘  │
│                                                                  │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐ │
│  │  High Scoring Venues    │  │  Toss Decision Trend (Season) │ │
│  │  (Column Chart)         │  │  (Stacked Column Chart)       │ │
│  └─────────────────────────┘  └───────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### Visual Specifications

#### 🃏 KPI Cards (Row 1)
| Card | Measure | Color |
|------|---------|-------|
| Total Venues | `DISTINCTCOUNT(Matches[venue])` | `#1F6FEB` |
| Bat 1st Win % | `Venue Bat First Win %` | `#F78166` |
| Chase Win % | `Venue Chase Win %` | `#3FB950` |
| Avg Runs/Match | `Venue Avg Runs` | `#E3B341` |

#### 📊 Venue Win %: Bat 1st vs Chase — 100% Stacked Bar
```
Visual Type    : 100% Stacked Bar Chart
Data:
  Y-Axis       : KPI_Venue[venue]
  Values       : KPI_Venue[bat_first_win_pct], KPI_Venue[chase_win_pct]
  Filter       : total_matches >= 10

Formatting:
  Color 1 (Bat First) : #F78166
  Color 2 (Chase)     : #3FB950
  Data Labels         : ON (percentage)
  Sort                : Desc by total_matches
  Title               : "Bat First vs Chase Win % by Venue"
```

#### 🍩 Toss Decision — Donut Chart
```
Visual Type    : Donut Chart
Data:
  Values       : [Chose to Bat], [Chose to Field]
  Legend       : "Bat", "Field"

Formatting:
  Color 1      : #F78166  (Bat)
  Color 2      : #3FB950  (Field)
  Inner Radius : 60%
  Center Label : "Toss Decision"
  Title        : "Toss Decision Overall"
```

#### 📊 High Scoring Venues — Column Chart
```
Visual Type    : Clustered Column Chart
Data:
  X-Axis       : KPI_Venue[venue]
  Y-Axis       : KPI_Venue[avg_runs_per_match]
  Tooltip      : KPI_Venue[total_runs], KPI_Venue[total_matches]

Formatting:
  Column Color : Gradient #1F6FEB → #E3B341 (high to low)
  Sort         : Desc by avg_runs_per_match
  Data Labels  : ON
  Reference Line: Overall average, Color=#F78166
  Title        : "Avg Runs per Match by Venue"
  X Labels     : Rotated 35°
```

#### 📈 Toss Decision Trend — Stacked Column by Season
```
Visual Type    : Stacked Column Chart
Data:
  X-Axis       : KPI_TossSeason[season]
  Y-Axis       : KPI_TossSeason[toss_win_pct]
  Legend       : "Bat", "Field" (from KPI_TossDecision)

Formatting:
  Color Bat    : #F78166
  Color Field  : #3FB950
  Data Labels  : ON
  Title        : "Toss Decision Trend by Season"
```

---

## 🎯 Slicer Panel Design (All Pages)

```
Recommended Slicers per Page:
  Page 1: Season (Dropdown)
  Page 2: Player (Search Dropdown), Season (Dropdown)
  Page 3: Bowler (Search Dropdown), Season (Dropdown)
  Page 4: Venue  (Dropdown)

Slicer Formatting (apply to all):
  Background    : #161B22
  Border Color  : #1F6FEB   (1px solid)
  Font          : Segoe UI, 10pt, #E6EDF3
  Header        : ON  |  Font: 9pt, #8B949E
  Clear Button  : ON  (Allow multi-select = ON)
```

---

## 🖱️ Interactivity Setup

### Visual Interactions (Edit Interactions mode)
```
Page 1:
  Season Slicer  → filters ALL visuals
  Team Bar       → highlights Donut & Column

Page 2:
  Player Slicer  → filters ALL visuals
  Top 10 Bar     → cross-highlights Line & Scatter

Page 3:
  Bowler Slicer  → filters ALL visuals
  Wickets Bar    → cross-highlights Economy & Dot Ball

Page 4:
  Venue Slicer   → filters ALL visuals
  Stacked Bar    → cross-filter Donut & Column
```

### Drill-Through Setup
```
From Page 2 (Batsman)  → Right-click any player bar
                       → Drill-through → Player Detail Page (optional)

From Page 3 (Bowler)   → Right-click any bowler bar
                       → Drill-through → Bowler Detail Page (optional)
```

---

## 💡 Power BI Design Best Practices

| Practice | Implementation |
|----------|---------------|
| **Consistent padding** | 8px padding inside all visuals |
| **Visual borders** | All visuals: Border ON, Color=#1F6FEB, Radius=6px |
| **Tooltips** | Custom tooltip page for match details on hover |
| **Bookmark** | Add "Reset Filters" button using bookmark |
| **Mobile layout** | Enable Phone Layout view for each page |
| **Performance** | Disable auto date hierarchy, reduce unnecessary columns |

---

## 📸 Page Thumbnail Colors (Tab Bar)

| Page | Tab Color |
|------|----------|
| Page 1 — Overall | `#1F6FEB` (Blue) |
| Page 2 — Batsman | `#F78166` (Orange) |
| Page 3 — Bowler  | `#3FB950` (Green) |
| Page 4 — Venue   | `#E3B341` (Gold) |

---

*Generated for IPL Performance Analytics Project — February 2026*
