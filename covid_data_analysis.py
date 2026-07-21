"""
covid_analysis.py - COVID-19 Data Analytics Project
Intermediate Level - No Dashboard, No Web Framework
Complete end-to-end data analysis pipeline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# ============================================================
# 1. CONFIGURATION
# ============================================================
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('viridis')

# Create charts directory
if not os.path.exists('charts'):
    os.makedirs('charts')

print("="*70)
print("🦠 COVID-19 DATA ANALYTICS PROJECT")
print("="*70)
print("\n📊 Starting analysis pipeline...\n")

# ============================================================
# 2. DATA COLLECTION
# ============================================================
print("📥 STEP 1: Fetching data from API...")

def fetch_covid_data():
    """Fetch COVID-19 data from disease.sh API"""
    try:
        url = "https://disease.sh/v3/covid-19/countries"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        print(f"   ✅ Successfully fetched data for {len(df)} countries")
        return df
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error fetching data: {e}")
        return None

df_raw = fetch_covid_data()

if df_raw is None:
    print("\n⚠️ Could not fetch data. Please check your internet connection.")
    exit()

# Save raw data
df_raw.to_csv('covid_data.csv', index=False)
print("   💾 Raw data saved to 'covid_data.csv'")

# ============================================================
# 3. DATA CLEANING
# ============================================================
print("\n🧹 STEP 2: Data Cleaning...")

# Select relevant columns
columns_needed = [
    'country', 'continent', 'population',
    'cases', 'todayCases', 'deaths', 'todayDeaths',
    'recovered', 'active', 'critical',
    'casesPerOneMillion', 'deathsPerOneMillion', 'recoveredPerOneMillion'
]

available_cols = [col for col in columns_needed if col in df_raw.columns]
df_clean = df_raw[available_cols].copy()
print(f"   ✅ Selected {len(available_cols)} columns")

# Handle missing values
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)

categorical_cols = df_clean.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df_clean[col] = df_clean[col].fillna('Unknown')

print("   ✅ Missing values handled")

# Remove duplicates
duplicates = df_clean.duplicated().sum()
if duplicates > 0:
    df_clean = df_clean.drop_duplicates()
print(f"   ✅ {duplicates} duplicates removed")

# Create calculated columns
df_clean['death_rate'] = (df_clean['deaths'] / df_clean['cases'] * 100).fillna(0)
df_clean['recovery_rate'] = (df_clean['recovered'] / df_clean['cases'] * 100).fillna(0)
df_clean = df_clean.replace([np.inf, -np.inf], 0)
print("   ✅ Calculated death_rate and recovery_rate")

# Save cleaned data
df_clean.to_csv('cleaned_data.csv', index=False)
print("   💾 Cleaned data saved to 'cleaned_data.csv'")
print(f"   📊 Final shape: {df_clean.shape}")

# ============================================================
# 4. EXPLORATORY DATA ANALYSIS
# ============================================================
print("\n📊 STEP 3: Exploratory Data Analysis...")

print(f"\n   📋 Dataset Overview:")
print(f"      Total Countries: {len(df_clean)}")
print(f"      Total Columns: {len(df_clean.columns)}")
print(f"      Columns: {', '.join(df_clean.columns)}")

# Global totals
print(f"\n   🌍 Global Totals:")
print(f"      Total Cases: {df_clean['cases'].sum():,.0f}")
print(f"      Total Deaths: {df_clean['deaths'].sum():,.0f}")
print(f"      Total Recovered: {df_clean['recovered'].sum():,.0f}")
print(f"      Total Active: {df_clean['active'].sum():,.0f}")
print(f"      Global Death Rate: {(df_clean['deaths'].sum() / df_clean['cases'].sum() * 100):.2f}%")

# Summary statistics
print(f"\n   📊 Summary Statistics:")
stats_cols = ['cases', 'deaths', 'recovered', 'active', 'death_rate', 'recovery_rate']
for col in stats_cols:
    if col in df_clean.columns:
        print(f"      {col}:")
        print(f"         Mean: {df_clean[col].mean():,.2f}")
        print(f"         Median: {df_clean[col].median():,.2f}")
        print(f"         Max: {df_clean[col].max():,.0f}")
        print(f"         Min: {df_clean[col].min():,.0f}")

# ============================================================
# 5. STATISTICAL ANALYSIS
# ============================================================
print("\n📈 STEP 4: Statistical Analysis...")

# Key metrics
metrics = {
    'Total Confirmed Cases': df_clean['cases'].sum(),
    'Total Deaths': df_clean['deaths'].sum(),
    'Total Recovered': df_clean['recovered'].sum(),
    'Total Active Cases': df_clean['active'].sum(),
    'Average Cases per Country': df_clean['cases'].mean(),
    'Maximum Cases (One Country)': df_clean['cases'].max(),
    'Minimum Cases (One Country)': df_clean['cases'].min()
}

print("\n   📊 Key Metrics:")
for key, value in metrics.items():
    print(f"      {key}: {value:,.0f}")

# Top countries by cases
print("\n   🏆 Top 10 Countries by Cases:")
top10_cases = df_clean.nlargest(10, 'cases')[['country', 'cases', 'deaths', 'recovered']]
for idx, row in top10_cases.iterrows():
    print(f"      {row['country']}: {row['cases']:,.0f} cases")

# Top countries by deaths
print("\n   💀 Top 10 Countries by Deaths:")
top10_deaths = df_clean.nlargest(10, 'deaths')[['country', 'deaths', 'cases']]
for idx, row in top10_deaths.iterrows():
    print(f"      {row['country']}: {row['deaths']:,.0f} deaths")

# Highest death rate
highest_death = df_clean.loc[df_clean['death_rate'].idxmax()]
print(f"\n   💀 Highest Death Rate: {highest_death['country']} - {highest_death['death_rate']:.2f}%")

# Highest recovery rate (countries with >100 cases)
df_filtered = df_clean[df_clean['cases'] > 100]
highest_recovery = df_filtered.loc[df_filtered['recovery_rate'].idxmax()]
print(f"   ❤️‍🩹 Highest Recovery Rate: {highest_recovery['country']} - {highest_recovery['recovery_rate']:.2f}%")

# ============================================================
# 6. FETCH HISTORICAL DATA
# ============================================================
print("\n📥 STEP 5: Fetching historical data...")

def fetch_historical_data():
    try:
        url = "https://disease.sh/v3/covid-19/historical/all?lastdays=365"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        df_hist = pd.DataFrame({
            'date': pd.to_datetime(list(data['cases'].keys())),
            'cases': list(data['cases'].values()),
            'deaths': list(data['deaths'].values()),
            'recovered': list(data['recovered'].values())
        })
        return df_hist
    except Exception as e:
        print(f"   ⚠️ Could not fetch historical data: {e}")
        return None

df_hist = fetch_historical_data()

# ============================================================
# 7. DATA VISUALIZATIONS
# ============================================================
print("\n📊 STEP 6: Creating Visualizations...")

# ---------- Chart 1: Cases Over Time ----------
if df_hist is not None and not df_hist.empty:
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df_hist['date'], df_hist['cases'], label='Total Cases', linewidth=2.5, color='#2ecc71')
    ax.plot(df_hist['date'], df_hist['deaths'], label='Total Deaths', linewidth=2.5, color='#e74c3c')
    ax.plot(df_hist['date'], df_hist['recovered'], label='Total Recovered', linewidth=2.5, color='#3498db')
    
    ax.set_title('COVID-19 Global Trends: Cases, Deaths, and Recoveries', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('charts/cases_over_time.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Chart 1 saved: charts/cases_over_time.png")

# ---------- Chart 2: Top 10 Countries by Cases ----------
fig, ax = plt.subplots(figsize=(12, 8))
top10_cases_plot = df_clean.nlargest(10, 'cases')
colors = plt.cm.plasma(np.linspace(0.2, 0.9, 10))

bars = ax.barh(top10_cases_plot['country'], top10_cases_plot['cases'], color=colors)
for bar, value in zip(bars, top10_cases_plot['cases']):
    ax.text(value, bar.get_y() + bar.get_height()/2, f'  {value:,.0f}', va='center', fontsize=10)

ax.set_title('Top 10 Countries by Confirmed COVID-19 Cases', fontsize=16, fontweight='bold')
ax.set_xlabel('Total Cases', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
ax.invert_yaxis()
ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/top10_countries_cases.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Chart 2 saved: charts/top10_countries_cases.png")

# ---------- Chart 3: Top 10 Countries by Deaths ----------
fig, ax = plt.subplots(figsize=(12, 8))
top10_deaths_plot = df_clean.nlargest(10, 'deaths')
colors = plt.cm.Reds(np.linspace(0.3, 0.9, 10))

bars = ax.barh(top10_deaths_plot['country'], top10_deaths_plot['deaths'], color=colors)
for bar, value in zip(bars, top10_deaths_plot['deaths']):
    ax.text(value, bar.get_y() + bar.get_height()/2, f'  {value:,.0f}', va='center', fontsize=10)

ax.set_title('Top 10 Countries by COVID-19 Deaths', fontsize=16, fontweight='bold')
ax.set_xlabel('Total Deaths', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
ax.invert_yaxis()
ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/top10_countries_deaths.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Chart 3 saved: charts/top10_countries_deaths.png")

# ---------- Chart 4: Deaths vs Recoveries Pie Chart ----------
fig, ax = plt.subplots(figsize=(10, 8))

global_deaths = df_clean['deaths'].sum()
global_recovered = df_clean['recovered'].sum()

labels = ['Deaths', 'Recovered']
sizes = [global_deaths, global_recovered]
colors_pie = ['#e74c3c', '#2ecc71']
explode = (0.05, 0.05)

wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                                  explode=explode, shadow=True, startangle=90,
                                  textprops={'fontsize': 12})

ax.legend([f'Deaths: {global_deaths:,.0f}', f'Recovered: {global_recovered:,.0f}'],
          loc='upper right', fontsize=10)

ax.set_title('Global COVID-19: Deaths vs Recoveries', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/deaths_vs_recoveries.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Chart 4 saved: charts/deaths_vs_recoveries.png")

# ---------- Chart 5: Distribution of Cases (Histogram) ----------
fig, ax = plt.subplots(figsize=(12, 7))

cases_filtered = df_clean[df_clean['cases'] > 0]['cases']
cases_filtered = cases_filtered[cases_filtered <= cases_filtered.quantile(0.95)]

ax.hist(cases_filtered, bins=50, color='#3498db', edgecolor='black', alpha=0.7)

ax.set_title('Distribution of Confirmed COVID-19 Cases (Top 95%)', fontsize=16, fontweight='bold')
ax.set_xlabel('Total Cases', fontsize=12)
ax.set_ylabel('Number of Countries', fontsize=12)
ax.grid(True, alpha=0.3)

mean_val = cases_filtered.mean()
median_val = cases_filtered.median()
ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:,.0f}')
ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:,.0f}')
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig('charts/cases_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Chart 5 saved: charts/cases_distribution.png")

# ---------- Chart 6: Correlation Heatmap ----------
corr_cols = ['cases', 'deaths', 'recovered', 'active', 'population', 
             'death_rate', 'recovery_rate', 'casesPerOneMillion', 'deathsPerOneMillion']

available_corr_cols = [col for col in corr_cols if col in df_clean.columns]
corr_df = df_clean[available_corr_cols].corr()

fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_df, dtype=bool))
sns.heatmap(corr_df, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            square=True, linewidths=0.5, ax=ax,
            cbar_kws={'shrink': 0.8})

ax.set_title('Correlation Matrix of COVID-19 Metrics', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Chart 6 saved: charts/correlation_heatmap.png")

# ============================================================
# 8. ANSWER ANALYTICAL QUESTIONS
# ============================================================
print("\n💡 STEP 7: Answering Analytical Questions...")
print("="*70)

# Q1: Highest confirmed cases
q1_country = df_clean.loc[df_clean['cases'].idxmax(), 'country']
q1_cases = df_clean['cases'].max()
print("\n1️⃣ Which country has the highest number of confirmed cases?")
print(f"   ✅ {q1_country} with {q1_cases:,.0f} cases")

# Q2: Highest deaths
q2_country = df_clean.loc[df_clean['deaths'].idxmax(), 'country']
q2_deaths = df_clean['deaths'].max()
print("\n2️⃣ Which country has the highest number of deaths?")
print(f"   ✅ {q2_country} with {q2_deaths:,.0f} deaths")

# Q3: Highest recovery rate (countries with >1000 cases)
df_1000 = df_clean[df_clean['cases'] > 1000]
if not df_1000.empty:
    q3_country = df_1000.loc[df_1000['recovery_rate'].idxmax(), 'country']
    q3_rate = df_1000['recovery_rate'].max()
    print("\n3️⃣ Which country has the highest recovery rate?")
    print(f"   ✅ {q3_country} with {q3_rate:.2f}% recovery rate")

# Q4: Highest death rate
q4_country = df_1000.loc[df_1000['death_rate'].idxmax(), 'country'] if not df_1000.empty else "N/A"
q4_rate = df_1000['death_rate'].max() if not df_1000.empty else 0
print("\n4️⃣ Which country has the highest death rate?")
print(f"   ✅ {q4_country} with {q4_rate:.2f}% death rate")

# Q5: Cases over time
if df_hist is not None and not df_hist.empty:
    df_hist['new_cases'] = df_hist['cases'].diff().fillna(0)
    peak_date = df_hist.loc[df_hist['new_cases'].idxmax(), 'date']
    peak_cases = df_hist['new_cases'].max()
    print("\n5️⃣ How have COVID-19 cases changed over time?")
    print(f"   📈 Peak daily cases: {peak_cases:,.0f} on {peak_date.strftime('%B %d, %Y')}")
    print(f"   📊 Total growth: {df_hist['cases'].iloc[-1]:,.0f} cases (from {df_hist['cases'].iloc[0]:,.0f})")
else:
    print("\n5️⃣ ⚠️ Historical data not available")

# Q6: Relationship between cases and deaths
correlation = df_clean['cases'].corr(df_clean['deaths'])
print("\n6️⃣ What is the relationship between confirmed cases and deaths?")
print(f"   📊 Correlation coefficient: {correlation:.3f}")
if correlation > 0.7:
    print("   ✅ Strong positive correlation: Countries with more cases tend to have more deaths")
elif correlation > 0.3:
    print("   ✅ Moderate positive correlation")
else:
    print("   ✅ Weak correlation")

# Q7: Most affected countries
print("\n7️⃣ Which countries were most affected by COVID-19?")
print("   ✅ Top 5 countries by cases:")
for i, (idx, row) in enumerate(df_clean.nlargest(5, 'cases').iterrows(), 1):
    print(f"      {i}. {row['country']}: {row['cases']:,.0f} cases, {row['deaths']:,.0f} deaths")

# Q8: Key insights
print("\n8️⃣ What insights can be drawn from the data?")
print("   ✅ See the Key Insights section below for detailed findings")

# ============================================================
# 9. KEY INSIGHTS AND CONCLUSIONS
# ============================================================
print("\n" + "="*70)
print("💡 KEY INSIGHTS AND CONCLUSIONS")
print("="*70)

insights = [
    "1. 🌍 GLOBAL IMPACT:",
    f"   - Total confirmed cases: {df_clean['cases'].sum():,.0f}",
    f"   - Total deaths: {df_clean['deaths'].sum():,.0f}",
    f"   - Global death rate: {(df_clean['deaths'].sum() / df_clean['cases'].sum() * 100):.2f}%",
    f"   - Global recovery rate: {(df_clean['recovered'].sum() / df_clean['cases'].sum() * 100):.2f}%",
    "",
    "2. 🏆 WORST AFFECTED COUNTRIES:",
    f"   - Most cases: {df_clean.loc[df_clean['cases'].idxmax(), 'country']} ({df_clean['cases'].max():,.0f})",
    f"   - Most deaths: {df_clean.loc[df_clean['deaths'].idxmax(), 'country']} ({df_clean['deaths'].max():,.0f})",
    "",
    "3. 📊 RATE ANALYSIS:",
    f"   - Highest death rate: {q4_country} ({q4_rate:.2f}%)",
    f"   - Highest recovery rate: {q3_country} ({q3_rate:.2f}%)" if not df_1000.empty else "   - Highest recovery rate: Not available",
    "",
    "4. 📈 TRENDS:",
    f"   - Cases vs Deaths correlation: {correlation:.3f}",
    "   - Distribution is highly skewed (few countries have most cases)",
    "   - Recovery rates vary significantly across countries",
    "",
    "5. 📋 RECOMMENDATIONS:",
    "   - Focus on countries with high death rates for healthcare support",
    "   - Study successful recovery strategies from countries with high recovery rates",
    "   - Monitor trends in countries with rapidly increasing cases"
]

for insight in insights:
    print(insight)

# ============================================================
# 10. SUMMARY
# ============================================================
print("\n" + "="*70)
print("✅ PROJECT COMPLETED SUCCESSFULLY!")
print("="*70)

print("\n📁 Files Created:")
print("   - covid_data.csv (raw data)")
print("   - cleaned_data.csv (cleaned data)")
print("   - charts/cases_over_time.png")
print("   - charts/top10_countries_cases.png")
print("   - charts/top10_countries_deaths.png")
print("   - charts/deaths_vs_recoveries.png")
print("   - charts/cases_distribution.png")
print("   - charts/correlation_heatmap.png")

print("\n📊 What We Accomplished:")
print("   ✅ Data Collection from API")
print("   ✅ Data Cleaning (missing values, duplicates, data types)")
print("   ✅ Exploratory Data Analysis")
print("   ✅ Statistical Analysis")
print("   ✅ 6 Data Visualizations")
print("   ✅ 8 Analytical Questions Answered")
print("   ✅ Key Insights Generated")

print("\n🛠️ Technologies Used:")
print("   - Python")
print("   - Pandas")
print("   - NumPy")
print("   - Matplotlib")
print("   - Seaborn")
print("   - Requests")

print("\n" + "="*70)
print("🦠 Project completed! Check the 'charts/' folder for visualizations.")
print("="*70)
