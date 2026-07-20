# 🦠 COVID-19 Data Analytics Project

A comprehensive, intermediate-level Python project analyzing COVID-19 data through data collection, cleaning, exploratory data analysis (EDA), statistical analysis, and data visualization.

---

## 📌 Project Overview

This project provides a complete end-to-end data analytics pipeline for COVID-19 pandemic data. It fetches real-time data from the disease.sh API, performs thorough data cleaning and preprocessing, conducts exploratory data analysis, calculates key statistical metrics, creates professional visualizations, and generates actionable insights.

The project demonstrates practical data analytics skills that employers seek, including data wrangling, statistical analysis, and data storytelling through visualizations.

---

## 🎯 Project Objectives

1. **Data Collection** – Fetch real-time COVID-19 data from the disease.sh API.
2. **Data Cleaning** – Handle missing values, remove duplicates, and format data correctly.
3. **Exploratory Data Analysis (EDA)** – Understand dataset structure, statistics, and distributions.
4. **Statistical Analysis** – Calculate total cases, deaths, recoveries, active cases, death rates, and recovery rates.
5. **Data Visualization** – Create 6 different charts to visualize findings.
6. **Analytical Questions** – Answer 8 key questions about the data.
7. **Key Insights** – Generate meaningful conclusions and recommendations.

---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| 🐍 **Python** | Main programming language |
| 📊 **Pandas** | Data manipulation and analysis |
| 🔢 **NumPy** | Numerical calculations |
| 📈 **Matplotlib** | Static visualizations |
| 🎨 **Seaborn** | Statistical visualizations |
| 🌐 **Requests** | API data fetching |

---

## 📁 Project Structure
COVID19_Data_Analytics/
│
├── covid_analysis.py # Main analysis script (everything in one file)
├── covid_data.csv # Raw data from API
├── cleaned_data.csv # Cleaned and processed dataset
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
└── charts/ # Saved visualizations
├── cases_over_time.png
├── top10_countries_cases.png
├── top10_countries_deaths.png
├── deaths_vs_recoveries.png
├── cases_distribution.png
└── correlation_heatmap.png

text

---

## 🚀 How to Run

### Prerequisites
- Python 3.7 or higher installed on your system.

### Installation & Execution

1. **Clone or download** this repository to your local machine.

2. **Navigate to the project directory**:
   ```bash
   cd COVID19_Data_Analytics
Install the required dependencies:

bash
pip install -r requirements.txt
Run the analysis script:

bash
python covid_analysis.py
View the results:

All analysis output appears in the terminal/console.

Charts are automatically saved in the charts/ folder.

Cleaned data is saved as cleaned_data.csv.

📊 What This Project Does
1. Data Collection
Fetches COVID-19 data from the disease.sh API

Saves raw data to covid_data.csv

2. Data Cleaning
Handles missing values (fills with 0 or appropriate values)

Removes duplicate records

Formats data types correctly

Creates calculated columns (death_rate, recovery_rate)

Saves cleaned data to cleaned_data.csv

3. Exploratory Data Analysis (EDA)
Displays dataset shape and column information

Shows summary statistics

Calculates global totals (cases, deaths, recoveries, active cases)

Identifies top countries by various metrics

4. Statistical Analysis
Total Confirmed Cases – Global total

Total Deaths – Global total

Total Recovered – Global total

Total Active Cases – Global total

Global Death Rate – Deaths / Cases × 100

Global Recovery Rate – Recovered / Cases × 100

Average Cases per Country

Maximum Cases (one country)

Minimum Cases (one country)

5. Data Visualizations (6 Charts)
Chart	Description
📈 Cases Over Time	Line chart showing global trends for cases, deaths, and recoveries
📊 Top 10 Cases	Horizontal bar chart of countries with highest confirmed cases
📊 Top 10 Deaths	Horizontal bar chart of countries with highest deaths
🥧 Deaths vs Recoveries	Pie chart comparing global deaths and recoveries
📊 Cases Distribution	Histogram showing how cases are distributed across countries
🔥 Correlation Heatmap	Heatmap showing relationships between different metrics
6. Analytical Questions Answered
Which country has the highest number of confirmed cases?

Answer provided with exact numbers.

Which country has the highest number of deaths?

Answer provided with exact numbers.

Which country has the highest recovery rate?

Answer provided with exact percentages.

Which country has the highest death rate?

Answer provided with exact percentages.

How have COVID-19 cases changed over time?

Visualized in the line chart with peak dates identified.

What is the relationship between confirmed cases and deaths?

Correlation coefficient calculated and explained.

Which countries were most affected by COVID-19?

Top 5 countries listed with their numbers.

What insights can be drawn from the data?

Comprehensive summary of key findings.

7. Key Insights Generated
Global Impact: Total cases, deaths, and recoveries worldwide.

Worst Affected Countries: Which countries had the highest impact.

Death Rate Analysis: Countries with the highest death rates.

Recovery Rate Analysis: Countries with the highest recovery rates.

Trend Analysis: How the pandemic progressed over time.

Correlation Insights: Relationship between different metrics.

Recommendations: Actionable suggestions based on the findings.

🔍 Sample Output (Terminal)
When you run the script, you'll see output like this:

text
======================================================================
🦠 COVID-19 DATA ANALYTICS PROJECT
======================================================================

📊 Starting analysis pipeline...

📥 STEP 1: Fetching data from API...
   ✅ Successfully fetched data for 220 countries

🧹 STEP 2: Data Cleaning...
   ✅ Selected 13 columns
   ✅ Missing values handled
   ✅ 0 duplicates removed
   ✅ Calculated death_rate and recovery_rate

📊 STEP 3: Exploratory Data Analysis...
   📋 Dataset Overview:
      Total Countries: 220
      Total Columns: 15

   🌍 Global Totals:
      Total Cases: 500,000,000+
      Total Deaths: 6,500,000+
      Total Recovered: 450,000,000+
      Global Death Rate: 1.30%

[... continues with full analysis ...]
📈 Visualizations Preview
Chart	Description
cases_over_time.png	Line chart with 3 lines (cases, deaths, recoveries) showing global trends
top10_countries_cases.png	Horizontal bar chart with 10 bars, color-coded from yellow to purple
top10_countries_deaths.png	Horizontal bar chart with 10 bars, color-coded in red shades
deaths_vs_recoveries.png	Pie chart with 2 slices (green for recovered, red for deaths)
cases_distribution.png	Histogram showing distribution with mean and median lines
correlation_heatmap.png	9x9 heatmap showing correlations between different metrics

💡 Key Insights Summary
Global Impact
Total Cases: Millions of confirmed cases worldwide

Total Deaths: Hundreds of thousands of deaths

Death Rate: Varies significantly by country

Recovery Rate: Varies significantly by country

Most Affected Countries
The United States leads in both cases and deaths

Several European and Asian countries have high numbers

Some smaller countries have extremely high death rates

Trends
Cases peaked during specific periods (winter months)

Strong positive correlation between cases and deaths

Recovery rates have improved over time




👤 Author
Your Name
🔗https://github.com/rayansalah-27
🔗https://www.linkedin.com/in/rayan-salah-013043375



📝 License
This project is open-source and available for educational purposes.
