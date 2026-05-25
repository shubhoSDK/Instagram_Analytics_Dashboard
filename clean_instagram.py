"""
Instagram Analytics — Data Cleaning Pipeline
=============================================
Handles:
  - Duplicate post & conversion IDs
  - Inconsistent content type labels (REELS, reel, Image)
  - Mixed boosted flags (Yes / Y / yes)
  - Mixed approval statuses (approved / Approved)
  - TBD / missing budgets
  - Negative revenue rows
  - Invalid campaign dates (end before start)
  - Mixed case payment statuses

Exports 5 clean CSVs ready for Power BI:
  IG_Posts_Clean.csv
  IG_Conversions_Clean.csv
  IG_Campaigns_Clean.csv
  IG_Daily_Clean.csv
  IG_Survey_Clean.csv

Usage:
  Place this script in the same folder as the Excel file, then run:
  python clean_instagram.py
"""

import pandas as pd
import numpy as np
import os

# ── Config ─────────────────────────────────────────────────────────────────
INPUT_FILE  = 'instagram_difficult_analysis_dataset.xlsx'
OUTPUT_DIR  = '.'   # change to a subfolder if needed e.g. 'clean_data'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Load all sheets ─────────────────────────────────────────────────────────
print("Loading workbook …")
xl = pd.ExcelFile(INPUT_FILE)

campaigns = pd.read_excel(xl, 'Campaigns')
posts     = pd.read_excel(xl, 'Posts_Raw')
daily     = pd.read_excel(xl, 'Daily_Profile_Metrics')
convs     = pd.read_excel(xl, 'Conversions_Orders')
survey    = pd.read_excel(xl, 'Audience_Survey')

print(f"  Campaigns : {campaigns.shape}")
print(f"  Posts     : {posts.shape}")
print(f"  Daily     : {daily.shape}")
print(f"  Conversions: {convs.shape}")
print(f"  Survey    : {survey.shape}")


# ══════════════════════════════════════════════════════════════════════════════
# 1. CAMPAIGNS
# ══════════════════════════════════════════════════════════════════════════════
print("\n[1/5] Cleaning Campaigns …")

# Parse dates (Excel serial or ISO string — both handled)
campaigns['Start_Date'] = pd.to_datetime(campaigns['Start_Date'], errors='coerce')
campaigns['End_Date']   = pd.to_datetime(campaigns['End_Date'],   errors='coerce')

# Budget: 'TBD' → NaN, then numeric
campaigns['Budget_INR'] = pd.to_numeric(campaigns['Budget_INR'], errors='coerce')

# Normalise approval status capitalisation
campaigns['Client_Approval_Status'] = (
    campaigns['Client_Approval_Status'].str.strip().str.capitalize()
)

# Derived columns
campaigns['Total_Cost_INR'] = (
    campaigns['Budget_INR'].fillna(0)
    + campaigns['Influencer_Cost_INR']
    + campaigns['Agency_Fee_INR']
)
campaigns['Duration_Days']      = (campaigns['End_Date'] - campaigns['Start_Date']).dt.days
campaigns['Invalid_Date_Flag']  = campaigns['Duration_Days'] < 0
campaigns['Budget_Missing_Flag']= campaigns['Budget_INR'].isna()

print(f"  TBD budgets flagged       : {campaigns['Budget_Missing_Flag'].sum()}")
print(f"  Invalid date ranges       : {campaigns['Invalid_Date_Flag'].sum()}")
print(f"  Approval values normalised: approved → Approved")


# ══════════════════════════════════════════════════════════════════════════════
# 2. POSTS
# ══════════════════════════════════════════════════════════════════════════════
print("\n[2/5] Cleaning Posts …")

pre_dedup   = len(posts)
posts_clean = posts.drop_duplicates(subset='Post_ID', keep='first').copy()
dup_posts   = pre_dedup - len(posts_clean)

# Normalise Content_Type labels
posts_clean['Content_Type'] = (
    posts_clean['Content_Type']
    .str.strip()
    .str.title()
    .replace({'Reels': 'Reel', 'Image': 'Static'})
)

# Normalise Boosted_Flag
posts_clean['Boosted_Flag'] = posts_clean['Boosted_Flag'].map(
    lambda x: 'Yes' if str(x).strip().lower() in ('yes', 'y') else 'No'
)

# Parse dates
posts_clean['Post_Date']    = pd.to_datetime(posts_clean['Post_Date'], errors='coerce')
posts_clean['Post_Month']   = posts_clean['Post_Date'].dt.to_period('M').astype(str)
posts_clean['Post_DayOfWeek'] = posts_clean['Post_Date'].dt.day_name()

# Derived engagement metrics
posts_clean['Engagement'] = (
    posts_clean[['Likes', 'Comments', 'Saves', 'Shares']]
    .sum(axis=1, skipna=True)
)
posts_clean['Engagement_Rate'] = (
    posts_clean['Engagement']
    / posts_clean['Reach'].replace(0, np.nan)
    * 100
).round(2)
posts_clean['Save_Rate'] = (
    posts_clean['Saves']
    / posts_clean['Reach'].replace(0, np.nan)
    * 100
).round(3)
posts_clean['Share_Rate'] = (
    posts_clean['Shares']
    / posts_clean['Reach'].replace(0, np.nan)
    * 100
).round(3)

print(f"  Duplicate posts removed   : {dup_posts}")
print(f"  Clean posts               : {len(posts_clean)}")
print(f"  Content type labels fixed : REELS/reel → Reel | Image → Static")
print(f"  Boosted flags normalised  : Yes/Y/yes → Yes")
print(f"  New cols added            : Engagement, Engagement_Rate, Save_Rate, Share_Rate, Post_Month, Post_DayOfWeek")


# ══════════════════════════════════════════════════════════════════════════════
# 3. CONVERSIONS
# ══════════════════════════════════════════════════════════════════════════════
print("\n[3/5] Cleaning Conversions …")

pre_c        = len(convs)
convs_clean  = convs.drop_duplicates(subset='Event_ID', keep='first').copy()
dup_convs    = pre_c - len(convs_clean)

# Revenue: coerce then drop negatives
convs_clean['Revenue_INR'] = pd.to_numeric(convs_clean['Revenue_INR'], errors='coerce')
neg_rev      = (convs_clean['Revenue_INR'] < 0).sum()
convs_clean  = convs_clean[convs_clean['Revenue_INR'] >= 0].copy()

# Normalise flags
convs_clean['Refund_Flag'] = convs_clean['Refund_Flag'].map(
    lambda x: 'Yes' if str(x).strip().lower() in ('yes', 'y') else 'No'
)
convs_clean['Payment_Status'] = convs_clean['Payment_Status'].str.strip().str.capitalize()

# Parse date
convs_clean['Event_Date'] = pd.to_datetime(convs_clean['Event_Date'], errors='coerce')

print(f"  Duplicate conversions removed: {dup_convs}")
print(f"  Negative revenue rows removed: {neg_rev}")
print(f"  Clean conversions            : {len(convs_clean)}")
print(f"  Payment status normalised    : paid → Paid")


# ══════════════════════════════════════════════════════════════════════════════
# 4. DAILY PROFILE METRICS
# ══════════════════════════════════════════════════════════════════════════════
print("\n[4/5] Cleaning Daily Metrics …")

daily['Date']             = pd.to_datetime(daily['Date'], errors='coerce')
daily['Net_Follower_Gain']= pd.to_numeric(daily['Net_Follower_Gain'], errors='coerce')
daily['Month']            = daily['Date'].dt.to_period('M').astype(str)
daily['DayOfWeek']        = daily['Date'].dt.day_name()

print(f"  Rows processed            : {len(daily)}")
print(f"  Algorithm change days     : {(daily['Algorithm_Change_Flag']=='Yes').sum()}")


# ══════════════════════════════════════════════════════════════════════════════
# 5. AUDIENCE SURVEY
# ══════════════════════════════════════════════════════════════════════════════
print("\n[5/5] Cleaning Survey …")

survey['Response_Date'] = pd.to_datetime(survey['Response_Date'], errors='coerce')

print(f"  Rows processed            : {len(survey)}")
print(f"  Avg purchase intent       : {survey['Purchase_Intent_1_5'].mean():.2f} / 5")
print(f"  Avg brand trust           : {survey['Brand_Trust_1_5'].mean():.2f} / 5")


# ══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ══════════════════════════════════════════════════════════════════════════════
print("\nExporting clean CSVs …")

exports = {
    'IG_Posts_Clean.csv'       : posts_clean,
    'IG_Conversions_Clean.csv' : convs_clean,
    'IG_Campaigns_Clean.csv'   : campaigns,
    'IG_Daily_Clean.csv'       : daily,
    'IG_Survey_Clean.csv'      : survey,
}

for filename, df in exports.items():
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(path, index=False)
    print(f"  ✅ {filename}  ({len(df)} rows, {len(df.columns)} cols)")


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
print("\n── CLEANING SUMMARY ─────────────────────────────────")
print(f"  Duplicate posts removed        : {dup_posts}")
print(f"  Duplicate conversions removed  : {dup_convs}")
print(f"  Negative revenue rows removed  : {neg_rev}")
print(f"  Campaigns with TBD budget      : {campaigns['Budget_Missing_Flag'].sum()}")
print(f"  Campaigns with invalid dates   : {campaigns['Invalid_Date_Flag'].sum()}")
print(f"  Content type labels normalised : REELS/reel/Image → Reel/Static")
print(f"  Boosted flags normalised       : Yes/Y/yes → Yes / No")
print(f"  Approval status normalised     : approved → Approved")
print(f"  Payment status normalised      : paid → Paid")
print(f"  New derived columns added      : Engagement, ER, Save_Rate, Share_Rate,")
print(f"                                   Post_Month, Post_DayOfWeek, Total_Cost_INR,")
print(f"                                   Duration_Days, Invalid_Date_Flag")
print(f"\n  5 clean CSVs ready for Power BI in: '{OUTPUT_DIR}/'")
print("─────────────────────────────────────────────────────")
