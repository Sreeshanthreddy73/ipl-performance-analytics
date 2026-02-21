# 🏏 IPL Performance Analytics & Interactive Dashboard System

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-green?logo=pandas)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?logo=powerbi)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

## 📌 Project Overview

An end-to-end **Data Analytics project** on the Indian Premier League (IPL) dataset —
covering data cleaning, KPI engineering in **Python (Pandas)**, and a **4-page interactive
Power BI dashboard** with player, team, venue, and toss insights.

> 🎯 Built as a placement-ready portfolio project demonstrating real-world data analytics skills.

---

## 📁 Project Structure

```
ipl-performance-analytics/
│
├── data/
│   ├── raw/                   # Original Kaggle datasets (not tracked in Git)
│   │   ├── matches.csv
│   │   └── deliveries.csv
│   └── processed/             # Cleaned & KPI-engineered datasets
│       ├── matches_cleaned.csv
│       ├── deliveries_cleaned.csv
│       ├── deliveries_enriched.csv
│       └── kpi_*.csv
│
├── scripts/
│   ├── 01_data_cleaning.py    # Data cleaning & preprocessing
│   ├── 02_kpi_engineering.py  # KPI calculations
│   └── 03_export_powerbi.py   # Final export for Power BI
│
├── powerbi/
│   └── IPL_Dashboard.pbix     # Power BI Dashboard file
│
├── docs/
│   ├── DAX_Formulas.md        # All DAX formulas used
│   ├── Dashboard_Design.md    # Layout & design guide
│   └── Viva_QnA.md            # Interview Q&A
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🗃️ Dataset

- **Source:** [Kaggle — IPL Complete Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)
- **Files Used:**
  - `matches.csv` — Match-level data (teams, venue, toss, result)
  - `deliveries.csv` — Ball-by-ball delivery data

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Pandas | Data cleaning & KPI engineering |
| NumPy | Numerical calculations |
| Power BI | Interactive dashboard |

---

## 📊 KPIs Engineered

| KPI | Description |
|-----|-------------|
| Team Win % | Wins / Total matches played per team |
| Toss Impact | % of matches where toss winner won the match |
| Strike Rate | (Batsman runs / Balls faced) × 100 |
| Boundary % | (4s + 6s) / Total balls faced × 100 |
| Economy Rate | Runs conceded / Overs bowled |
| Dot Ball % | Dot balls / Total balls bowled × 100 |
| Venue Win % | Win ratio per venue |
| Bat First vs Chase | Win % when batting first vs chasing |

---

## 📈 Power BI Dashboard Pages

| Page | Content |
|------|---------|
| **Page 1** | Overall Tournament Insights — totals, win %, toss impact |
| **Page 2** | Batsman Analysis — top scorers, strike rate, boundaries |
| **Page 3** | Bowler Analysis — wickets, economy, dot balls |
| **Page 4** | Venue & Toss Analysis — venue stats, toss trends |

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Sreeshanthreddy73/ipl-performance-analytics.git
cd ipl-performance-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place raw datasets in data/raw/
#    (Download from Kaggle link above)

# 4. Run scripts in order
python scripts/01_data_cleaning.py
python scripts/02_kpi_engineering.py
python scripts/03_export_powerbi.py
```

---

## 📄 Resume Description

> **IPL Performance Analytics & Interactive Dashboard System** *(Python · Power BI · Pandas)*
> Built an end-to-end data analytics pipeline on 7+ seasons of IPL data (500K+ rows). Performed
> data cleaning, team name standardization, and feature engineering using Python/Pandas. Engineered
> 10+ KPIs including strike rate, economy rate, toss impact, and venue win percentage. Designed a
> 4-page interactive Power BI dashboard with dynamic slicers, DAX measures, and drill-through
> filters enabling real-time player, team, and venue performance analysis.

---

## 👨‍💻 Author
**Sreeshanthreddy** — CSE Student | [GitHub](https://github.com/Sreeshanthreddy73)
