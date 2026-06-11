---
name: advanced-analytics
description: End-to-end workflow for structured data analytics projects from raw CSV, SQL, or Excel data to cleaned datasets, exploratory analysis, statistical or machine learning models, driver analysis, charts, reports, and executive-ready business insights. Use when Codex needs to analyze datasets, perform EDA, build segmentation, scoring, regression, classification, clustering, forecasting, or translate findings into recommendations.
---

# Advanced Analytics

Use this skill to run an analytics project from raw data to decision-ready conclusions. Prioritize reproducibility, clear assumptions, and business interpretation over lengthy technical narration.

## Operating Principles

- Start by clarifying the business question, decision, audience, grain of analysis, and success metric.
- Inspect the data before modeling or summarizing; verify schema, types, row counts, keys, time ranges, missingness, duplicates, and obvious anomalies.
- Prefer Python with `pandas`, `numpy`, `scikit-learn`, and plotting libraries for local files. Prefer SQL for heavy warehouse transformations when the data lives in a database.
- Keep code modular and rerunnable. Separate loading, cleaning, feature engineering, analysis, modeling, and reporting steps.
- Treat leakage, sampling bias, date cutoffs, target definition, and population mismatch as first-class risks.
- Translate every important technical result into practical business language.

## Workflow

### 1. Understand the Data

- Load only the needed files, sheets, or SQL tables.
- Inspect shape, schema, types, missing values, unique counts, value ranges, date coverage, and target availability.
- Identify entity keys, time keys, joins, target variable, unit of observation, and whether records are independent.
- Flag data quality issues such as duplicated keys, impossible values, mixed units, inconsistent categories, outliers, and target leakage candidates.

### 2. Prepare the Data

- Handle missing values using a stated approach: preserve as signal, impute, exclude, or create missingness flags.
- Standardize categories, dates, numeric units, and boolean fields.
- Encode categorical features only after preserving interpretable labels for reporting.
- Create derived features that reflect business mechanisms, such as tenure, recency, frequency, monetary value, utilization, growth, lagged behavior, or ratios.
- Split train/test data with respect to time when the business use case is forward-looking.

### 3. Explore and Profile

- Produce summary statistics and distributions for core metrics.
- Compare target rates or outcomes across meaningful segments.
- Examine correlations, monotonic relationships, seasonality, cohort behavior, and interaction patterns.
- Use charts and tables selectively; each visual should answer a business question.
- Track surprising findings separately from confirmed findings.

### 4. Model When Useful

Choose the simplest model that answers the question:

- Use regression for continuous targets; report RMSE, MAE, residual patterns, and practical error size.
- Use classification for binary or multiclass targets; report AUC, precision/recall, lift, calibration, confusion matrix, and threshold tradeoffs where relevant.
- Use clustering for segmentation; scale numeric features, choose an interpretable number of clusters, and profile clusters in business terms.
- Use time series methods when ordering, trend, seasonality, holidays, or lag effects matter.
- For credit scoring, consider WOE, IV, logistic regression, score scaling, AUC, KS, stability, and explainability.

Always compare against a baseline and explain whether added complexity improves the business decision enough to justify it.

### 5. Identify Drivers

- Use model coefficients, permutation importance, tree importance, SHAP-style explanations, partial dependence, or segment deltas as appropriate.
- Distinguish association from causation unless the design supports causal claims.
- Group variables into business categories such as customer profile, engagement, product usage, pricing, operations, risk, or channel.
- Quantify impact in understandable units where possible, such as conversion lift, expected revenue, churn probability, or cost reduction.

### 6. Interpret for the Business

- State what changed, who or what is affected, why it matters, and what action follows.
- Separate facts, model-based estimates, assumptions, and recommendations.
- Identify risks, opportunities, data limitations, and next measurements to collect.
- Prefer concise executive conclusions supported by reproducible details.

## Output Standard

Always provide:

- Reproducible Python or SQL used for the analysis, unless the user only asked for a conceptual review.
- A short data quality summary.
- Key insights with evidence and business interpretation.
- Charts or tables when they improve understanding.
- Clear recommendations, expected impact, caveats, and next steps.

For deliverables, put the executive summary first, then the supporting analysis. Avoid presenting metric dumps without interpretation.
