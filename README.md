# Instagram_Analytics_Dashboard
Instagram Analytics Dashboards | Data cleaned with Python | pandas | Visualised with Chart.js | Power BI ready
# 📊 Instagram Analytics Dashboard

> **End-to-end data cleaning, analysis, and interactive dashboard for 6 Instagram accounts — built entirely in Python and visualised with Chart.js.**

🔗 **[Open Live Dashboard →](https://YOUR-USERNAME.github.io/REPO-NAME/IG_Dashboard_A4.html)**

---

## 🗂 Project Overview

A real-world messy Instagram dataset covering **6 brand accounts**, **668 posts**, **866 conversions**, and **60 paid campaigns** across Jul–Dec 2025. The goal: clean the data, uncover what actually drives reach, engagement, and revenue — and deliver a print-ready A4 dashboard.

| Sheet | Raw Rows | After Cleaning |
|---|---|---|
| Posts_Raw | 668 | 643 |
| Conversions_Orders | 866 | 836 |
| Campaigns | 60 | 60 |
| Daily_Profile_Metrics | 653 | 653 |
| Audience_Survey | 350 | 350 |

---

## 🧹 Data Quality Issues Fixed

| Issue | Count | Fix Applied |
|---|---|---|
| Duplicate post IDs | 25 | Kept first occurrence |
| Duplicate conversion IDs | 16 | Kept first occurrence |
| Negative revenue rows | 14 | Removed |
| TBD / missing budgets | 3 | Flagged as `NaN` |
| Invalid campaign dates (end < start) | 3 | Flagged |
| Inconsistent content type labels | `REELS`, `reel`, `Image` | Normalised → `Reel`, `Static` |
| Mixed boosted flags | `Yes`, `Y`, `yes` | Normalised → `Yes` / `No` |
| Mixed approval status | `approved`, `Approved` | Normalised → `Approved` |
| Missing UTM tags | 82 posts | Flagged in `Quality_Flag` |

---

## 📈 Key Insights

### Content Performance
- **Reels** deliver the highest average reach — **25,511** per post (2.1× more than Stories)
- **Carousels** win on engagement rate — **6.2%** (highest of any format)
- **Static posts** and **Stories** lag significantly in both reach and ER

### Boosted vs Organic
- Boosted posts average **22K reach** vs **15K organic** — a 45% uplift
- Yet organic ER (**4.4%**) slightly outperforms boosted (**4.3%**) — reach ≠ connection

### Conversion Funnel (avg per post)
```
17,142 Reach  →  362 Profile Visits  →  100 Link Clicks  →  45 Follows
                    ↓ 97.9% drop-off          ↓ 72% drop-off      ↓ 55% drop-off
```
> Link-click CTR is the primary bottleneck in the funnel.

### Algorithm Impact
- Normal days avg follower gain: **217**
- Algorithm-change days avg follower gain: **27**
- **88% crash** — pausing paid boosts on those days avoids wasted spend

### Audience Survey Signals
- **Tier 3 cities** score highest purchase intent (**3.71 / 5**) vs Metro (**2.73 / 5**)
- **Word-of-mouth** is the #1 discovery channel (63 responses) — ahead of Reels and Influencer
- Top interests: Food, Fashion, Education, Tech, Beauty

### Revenue (7-day attribution, paid, no refunds)
| Account | Revenue (₹) |
|---|---|
| SareeStreet | 48,572 |
| CafeCanvas | 41,780 |
| ByteBazaar | 41,689 |
| GlowKart | 36,182 |
| FitFuel India | 25,788 |
| UrbanPaws | 5,896 |

---

## 💡 Recommendations

1. **Shift 30% of Static budget to Carousels** — same spend, higher engagement rate
2. **Target Tier 2 & 3 cities** — purchase intent is 36% higher than Metro audiences
3. **Pause paid boosts on algorithm-change days** — follower gain drops 88%, spend is wasted
4. **Add referral hooks to Reels captions** — word-of-mouth beats every paid channel
5. **Fix UTM tagging on 82 posts** — missing attribution is hiding real campaign ROI

---

## 🗃 Files in This Repo

```
├── IG_Dashboard_A4.html        # Interactive A4 dashboard (live via GitHub Pages)
├── clean_instagram.py          # Full Python cleaning pipeline
├── IG_Posts_Clean.csv          # Cleaned posts data — Power BI ready
├── IG_Conversions_Clean.csv    # Cleaned conversions — Power BI ready
├── IG_Campaigns_Clean.csv      # Cleaned campaigns — Power BI ready
├── IG_Daily_Clean.csv          # Cleaned daily profile metrics
└── IG_Survey_Clean.csv         # Cleaned audience survey responses
```

---

## 🛠 Tech Stack

| Layer | Tool |
|---|---|
| Data cleaning | Python 3 · pandas · numpy |
| Geographic validation | geonamescache |
| Dashboard | HTML · CSS · Chart.js 4.4 |
| BI export | CSV → Power BI |
| Hosting | GitHub Pages |

---

## 🚀 Run the Cleaning Pipeline Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
cd REPO-NAME

# 2. Install dependencies
pip install pandas numpy geonamescache openpyxl

# 3. Place the raw Excel file in the same directory
# instagram_difficult_analysis_dataset.xlsx

# 4. Run
python clean_instagram.py
```

Clean CSVs will be exported to the same directory.

---

## 📌 Dashboard Preview

> Open `IG_Dashboard_A4.html` in Chrome and press `Ctrl+P` → A4 · No margins · Background graphics ON to export a clean 2-page PDF.

**Page 1** — Reach by content type · Account comparison · Boosted vs Organic · Revenue · Conversion funnel · Monthly follower trend

**Page 2** — Campaign objectives · Discovery sources · Algorithm impact · Purchase intent by city tier · Narrative insights · Client recommendations table

---

## 👤 Author

Built as part of a data analytics portfolio project.
Connect on https://www.linkedin.com/in/shubhodeep-kundu-981a28402
NOTE :- used Claude for thr readme generation and understanding the datasets.

---

*Dataset is synthetic and designed for advanced analytics practice. All figures are from the cleaned dataset.*
