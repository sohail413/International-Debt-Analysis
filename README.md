# International Debt Analysis System Using Python, SQL, and Visualization Tools

## 📌 Domain
Finance Analytics & Global Economic Data Analysis

## 📖 Problem Statement
Global financial institutions and organizations such as the World Bank generate vast amounts of data related to international debt, including country-wise borrowings, repayments, interest payments, and other financial indicators. However, this data is often stored in raw and complex formats such as CSV files with multiple indicators, making it difficult to analyze, interpret, and extract meaningful insights.

The challenge lies in transforming this raw financial data into a structured and usable format by performing data cleaning, preprocessing, and exploratory data analysis (EDA). Ensuring data quality, handling missing values, and organizing the data efficiently are critical steps before performing any meaningful analysis.

This project aims to build a complete **end-to-end data analytics pipeline** that enables:
- Cleaning and preprocessing international debt data using Python
- Performing exploratory data analysis (EDA) to identify key trends and patterns
- Storing processed data in a structured SQL database
- Writing SQL queries to extract meaningful insights
- Developing interactive dashboards using Streamlit (Plotly / Seaborn / Matplotlib) or Power BI for data visualization and reporting

## 🎯 Objective
Design and implement an **International Debt Analytics System** that follows the complete data lifecycle:
1. Data Collection
2. Data Cleaning & Preprocessing
3. Exploratory Data Analysis (EDA)
4. Data Storage (SQL)
5. Data Visualization (Power BI / Streamlit)

## 🛠️ Skills Takeaway
- Python & Data Processing
- CSV to DataFrame Conversion
- Data Cleaning (Handling Missing Values & Duplicates)
- Data Preprocessing & Transformation
- Exploratory Data Analysis (EDA)
- Financial Data Understanding (Country-wise Debt Analysis)
- MySQL & SQL Queries
- Data Modeling & Relationships
- Data Visualization (Plotly / Seaborn / Matplotlib)
- Dashboard Development (Streamlit / Power BI)
- End-to-End Data Analytics Pipeline

## 🗂️ Approach

### 1. Data Collection
- Import the dataset in CSV format
- Load the dataset into Python using Pandas DataFrame
- Understand the structure, columns, and data types

### 2. Data Preprocessing
- Handle missing values (null data)
- Remove duplicate records
- Perform data type conversion
- Filter relevant columns (country, indicators, debt values)
- Standardize and clean the dataset

### 3. Exploratory Data Analysis (EDA)
- Analyze country-wise debt distribution
- Identify top countries with highest and lowest debt
- Explore different debt indicators and their impact
- Identify patterns, trends, and relationships
- Perform statistical summaries and comparisons

### 4. Database Design & SQL Integration
- Design relational tables (Countries, Indicators, Debt Data)
- Create database using MySQL
- Insert cleaned data into SQL tables
- Write SQL queries for analysis
- Apply primary key and foreign key relationships

### 5. Data Visualization
- Connect SQL database to Power BI or a Streamlit application
- Create dashboards using Plotly / Seaborn / Matplotlib
- Build visual insights for country-wise and indicator-wise debt analysis

### 6. Insights & Reporting
Generate insights on:
- Country-wise debt distribution
- Top countries with highest and lowest debt
- Debt distribution across different indicators
- Trends and patterns in international debt
- Support data-driven decision making

## 📊 Dataset
**Dataset:** International Debt Statistics (Jan 2022)

## 🧮 SQL Analytical Questions (30)

### Basic Queries
1. Retrieve all distinct country names from the dataset.
2. Count the total number of countries available.
3. Find the total number of indicators present.
4. Display the first 10 records of the dataset.
5. Calculate the total global debt.
6. List all unique indicator names.
7. Find the number of records for each country.
8. Display all records where debt is greater than 1 billion USD.
9. Find the minimum, maximum, and average debt values.
10. Count total number of records in the dataset.

### Intermediate Level
1. Find the total debt for each country.
2. Display the top 10 countries with the highest total debt.
3. Find the average debt per country.
4. Calculate total debt for each indicator.
5. Identify the indicator contributing the highest total debt.
6. Find the country with the lowest total debt.
7. Calculate total debt for each country and indicator combination.
8. Count how many indicators each country has.
9. Display countries whose total debt is above the global average.
10. Rank countries based on total debt (highest to lowest).

### Advanced Level
1. Find the top 5 indicators contributing most to global debt.
2. Calculate percentage contribution of each country to total global debt.
3. Identify the top 3 countries for each indicator based on debt.
4. Find the difference between maximum and minimum debt for each country.
5. Create a view for the top 10 countries with highest debt.
6. Categorize countries into High Debt, Medium Debt, and Low Debt (based on thresholds).
7. Use window functions to calculate cumulative debt per country.
8. Find indicators where average debt is higher than overall average debt.
9. Identify countries contributing more than 5% of global debt.
10. Find the most dominant indicator (highest contribution) for each country.

## ✅ Results
- Structured relational database for international debt data
- Clean and preprocessed dataset (handled missing values & duplicates)
- Successful CSV to DataFrame conversion
- Integrated Python with MySQL database
- Effective country-wise debt analysis
- Interactive dashboard using Streamlit / Power BI
- Insightful data visualization (Plotly / Seaborn / Matplotlib)
- Identification of top and least indebted countries
- Indicator-wise and country-wise debt insights
- End-to-end data analytics pipeline implementation

## 📏 Project Evaluation Metrics
- Proper data preprocessing (handling missing values & duplicates)
- Accurate CSV to DataFrame conversion
- Effective Exploratory Data Analysis (EDA)
- Correct database design & normalization
- Proper implementation of table relationships (Primary Key & Foreign Key)
- SQL query optimization and performance
- Effective use of joins and aggregations
- Data integration (Python to MySQL)
- Visualization quality and clarity (Plotly / Seaborn / Matplotlib)
- Dashboard functionality (Streamlit / Power BI)
- Clean and well-structured Python code
- Insight generation and interpretation

## 🏷️ Technical Tags
Python, CSV Data Handling, Data Preprocessing, Exploratory Data Analysis (EDA), MySQL, SQL, Data Modeling, Data Integration, Plotly, Seaborn, Matplotlib, Streamlit Dashboard, Power BI, Finance Analytics, Economic Data Analysis, International Debt Analysis.

## 📦 Project Deliverables
- CSV dataset (raw data file)
- Cleaned and preprocessed dataset (CSV / DataFrame)
- Complete MySQL database schema
- Data insertion into SQL tables
- 30 SQL analytical queries
- Python script for data processing & integration
- Data visualization (Plotly / Seaborn / Matplotlib)
- Interactive dashboard (Streamlit / Power BI)
- EDA report with insights
- Final documentation file

## 📋 Project Guidelines
- Follow proper data preprocessing (handle missing values & duplicates)
- Ensure correct CSV to DataFrame conversion
- Perform meaningful Exploratory Data Analysis (EDA)
- Design a normalized relational database (MySQL)
- Maintain proper table relationships (Primary & Foreign Keys)
- Ensure accurate data insertion from Python to SQL
- Write optimized SQL queries using joins and aggregations
- Use appropriate visualization tools (Plotly / Seaborn / Matplotlib)
- Build a structured dashboard (Streamlit or Power BI)
- Maintain clean, readable, and modular Python code
- Generate clear insights from the analysis
- Provide well-structured documentation

