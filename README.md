# StockWise — Inventory Demand Forecasting & Reorder Recommendation System

An independent Python project exploring inventory demand forecasting and reorder recommendations using historical transaction data.

## Overview

StockWise investigates how data analysis, statistical forecasting, machine learning, and inventory management logic can support stock planning.

The current focus is on:
- Cleaning and validating transaction data
- Building daily product-level demand series
- Profiling product demand and intermittency
- Evaluating forecasting baselines
- Preparing for statistical and machine-learning forecasting

Inventory and reorder recommendation functionality will be developed after the forecasting stage.

### Data Source

The project uses the [UCI Online Retail dataset](https://doi.org/10.24432/C5BW33) for demonstrative purposes.

**Citation:** Chen, D. (2015). *Online Retail*. UCI Machine Learning Repository.  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The dataset contains transaction data from a UK-based online retailer. The original data is not included in this repository, and `data/raw/` is excluded from version control. The dataset's authors and UCI are not affiliated with or endorsing StockWise.

Inventory levels, supplier lead times, safety-stock parameters, and other business-specific information are not provided by the source dataset; some may be generated synthetically later.

## Project Status

**Status:** In Development

The current stage covers data preparation, demand analysis, forecasting baselines, and preparation for machine-learning forecasting.

## Features

### Data Preparation and Transaction Classification

The source dataset contains 541,909 transaction lines, 4,070 unique products, 25,900 unique invoices, and 9,288 cancellation invoices. It spans December 2010 to December 2011 and includes missing product descriptions, missing `CustomerID` values, and 10,624 negative-quantity transactions.

The source is transaction-oriented rather than a complete inventory-management model. Negative quantities may represent cancellations, returns, damages, discarded stock, or other adjustments. Descriptions such as `"thrown away"`, `"Unsaleable, destroyed."`, `"damages"`, `"Manual"`, and `"check"` illustrate why these records cannot all be interpreted as customer returns.

The current classification is:

| Transaction type | Identification | Demand treatment |
|---|---|---|
| Sale | `Quantity > 0` | Included |
| Cancellation | `InvoiceNo` starts with `C` | Excluded |
| Other negative transaction | Negative quantity without a cancellation invoice | Excluded |

The UCI dataset documentation identifies invoice numbers beginning with `C` as cancellations.

Demand is defined as the sum of positive sales quantities. Consequently, `daily_sales.csv` represents product demand under this definition, not a complete record of physical inventory movements.

#### Cancellation Matching

An exploratory matching method compared cancellations with earlier sales using `StockCode`, `UnitPrice`, absolute `Quantity`, `InvoiceDate`, a limited time window, and one-to-one matching.

The method was rejected for production cleaning because the source data does not provide an explicit link between a cancellation and its original sale. Matching attributes can provide evidence of a relationship but cannot reliably establish it in every case. The current pipeline therefore excludes cancellation records without automatically removing potentially corresponding positive sales.

#### Exceptional Demand and Outlier Investigation

High-volume product-day observations were investigated rather than automatically removed.

- **Product `23843`:** A positive transaction of 80,995 units was followed 12 minutes later by a cancellation with the same quantity and unit price. This is strong evidence of a reversal, but the records are not explicitly linked in the source data. The positive quantity remains in the current demand dataset.
- **Product `84826`:** A demand quantity of 12,540 units was recorded on 25 November 2011. No corresponding cancellation was identified during the investigation, so the observation was retained.
- **Product `84611B`:** A positive quantity of 1,287 and a negative quantity of 1,430, described as `"thrown away"`, were recorded at the same timestamp with zero unit prices. This appears to be an operational inventory event, although its precise meaning remains uncertain.

These cases show why unusual quantities must be investigated in context. Their magnitude alone does not establish whether they are invalid, ordinary demand, or exceptional business events.

The current approach is to preserve unusual observations unless an implemented cleaning rule excludes them, investigate extreme quantities, report deviations transparently, and evaluate their impact on forecasting performance. Outlier detection and any future adjustments will be considered separately from transaction cleaning.

#### Zero-Price Transaction Analysis

An exploratory investigation examined positive-quantity transactions with `UnitPrice = 0`. It compared product descriptions against normal-price sales to identify administrative notes, corrections, stock adjustments, and other suspicious descriptions.

Remaining records were compared by `StockCode`, including zero-price transaction counts and quantities, maximum transaction quantities, normal-price transaction counts, and normal sales medians and maxima. Products such as `84826`, `46000S`, `23157`, and `46000M` were identified for further investigation.

A recognisable description does not prove that a transaction represents ordinary demand. Zero-price transactions have not yet been given a dedicated classification rule in the production pipeline, so positive-quantity zero-price records remain included under the current demand definition.

### Processing Workflow and Project Organization

The current processing workflow is:

    Online Retail.xlsx
           |
           v
    Data Quality Analysis
           |
           v
    Transaction Classification
           |
           v
    Aggregate Positive Sales
    by Date and StockCode
           |
           v
    data/processed/daily_sales.csv

Data cleaning is implemented in `scripts/clean_data.py`. The main project runner is `stockwise.py`.

The `analysis/` directory preserves the earlier script-based workflow:

    analysis/
        01_inspect_data.py
        02_data_quality.py
        03_inspect_product.py
        04_inspect_processed_data.py
        05_inspect_demand.py
        06_inspect_cancellations.py
        07_inspect_forecasting_dataset.py
        08_evaluate_baseline.py
        09_profile_demand.py

Ongoing exploratory, validation, and forecasting work is primarily performed in Jupyter notebooks:

    notebooks/
        raw_data_analysis.ipynb
        clean_data_analysis.ipynb
        forecasting_analysis.ipynb

The notebooks are the primary location for ongoing analysis; the existing scripts remain available for reference.

### Data Model

The processed `daily_sales.csv` dataset contains:

| Field | Description |
|---|---|
| `Date` | Transaction date |
| `StockCode` | Product identifier |
| `Demand` | Total positive sales quantity for the product on that date |

The source data also includes invoice numbers, descriptions, quantities, invoice dates, unit prices, customer IDs, and country. It does not provide a complete inventory model.

### Current Data Preparation Status

Completed work includes:

- Raw-data inspection and analysis of missing values and negative quantities.
- Classification of sales, cancellations, and other negative transactions.
- Investigation and rejection of unreliable cancellation-to-sale matching for production cleaning.
- Definition of demand as positive sales quantities.
- Investigation of exceptional demand observations and zero-price transactions.
- Generation of the processed daily-demand dataset.
- Creation of continuous daily time series within each product's observed activity period, filling internal gaps with zero demand.
- Validation of product-history boundaries and confirmation that zero-demand observations do not extend beyond those boundaries.
- Validation of missing values and preservation of total demand across the aggregated and continuous forecasting datasets.
- Verification that the cleaning and daily-demand generation functions produce identical results when run repeatedly on the same input.
- Separation of the cleaning script from exploratory analysis and migration of ongoing work to Jupyter notebooks.
- Evaluation of a 7-day seasonal-naive baseline and profiling of product-level demand.

The continuous forecasting dataset contains:

| Measure | Result |
|---|---:|
| Products | 3,941 |
| Product-day observations | 1,077,874 |
| Date range | 2010-12-01 to 2011-12-09 |
| Zero-demand product-days | 801,031 |
| Positive-demand product-days | 276,843 |
| Zero-demand observations | 74.4% |
| Total positive demand preserved | 5,660,981 units |

The total positive demand is preserved across the raw positive-sale transactions, aggregated daily sales, and continuous forecasting dataset. Adding zero-demand days does not change the total.

### Demand Forecasting Analysis

Forecasting development begins with statistical analysis to understand product-level demand characteristics and establish benchmarks before evaluating machine-learning models.

#### Continuous Product Time Series

For each product, the forecasting dataset covers its observed activity period:

- The first observed sale defines the beginning of the period.
- The last observed sale defines the end.
- Missing dates within that period are filled with `Demand = 0`.
- Dates outside the observed period are not artificially added.

Validation confirmed that product-history boundaries are preserved and zero-demand observations occur only within those boundaries.

#### Baseline Forecast

The initial benchmark is a 7-day seasonal-naive forecast:

    Forecast(t) = Demand(t - 7)

Each forecast uses the demand recorded seven days earlier. Evaluation uses a chronological 80/20 time-based split rather than a random split.

| Metric | Result |
|---|---:|
| Cutoff date | 2011-09-26 |
| Training rows | 843,845 |
| Test rows | 207,492 |
| MAE | 10.11 |
| RMSE | 62.37 |

The baseline is retained as a reference point for subsequent statistical and machine-learning forecasting methods.

#### Statistical Demand Profile

Across the 3,941 products:

- Average active history: approximately 274 days
- Median active history: 353 days
- Average zero-demand percentage: approximately 70.5%
- Median zero-demand percentage: approximately 78.4%
- Average positive-demand percentage: approximately 29.5%
- Median positive-demand percentage: approximately 21.6%
- Average coefficient of variation: approximately 4.36
- Median coefficient of variation: approximately 3.75

Demand is highly intermittent, skewed, and variable. Many products have zero demand on most observed days. For example, product `79151B` has only two positive-demand days across 359 active days.

Examples of highly variable demand include:

- **Product `84826`:** Mean demand approximately 36.94 units, standard deviation approximately 651.14, maximum 12,540 units.
- **Product `23166`:** Mean demand approximately 239.37 units, median demand 0, maximum 74,215 units.
- **Product `23843`:** One observed active day with demand of 80,995 units.

The dataset contains frequent zero-demand periods, intermittent demand, high variability, strong right-skewness, extreme demand events, and products with very different amounts of historical information.

These characteristics motivate evaluating statistical and intermittent-demand forecasting methods before relying on machine-learning models.

### Machine Learning

Machine-learning forecasting models will be evaluated after the statistical forecasting stage.

Potential candidate models include:

- Linear Regression
- Random Forest
- Gradient Boosting

Potential forecasting features include:

- Historical demand lags
- Rolling demand statistics
- Day of week
- Month
- Other relevant product or transaction features identified during analysis

Models will be evaluated using chronological time-based validation and compared against the established statistical baselines rather than evaluated in isolation.

## Technology Stack

- Python 3.14
- pandas
- NumPy
- scikit-learn
- JupyterLab

Additional libraries will be added only when justified by the project requirements.

## Project Structure

    StockWise/
    ├── analysis/
    │   ├── __init__.py
    │   ├── 01_inspect_data.py
    │   ├── ...
    │   ├── 08_evaluate_baseline.py
    │   └── 09_profile_demand.py
    ├── core/
    │   └── forecasting/
    │       ├── evaluation.py
    │       ├── profiling.py
    │       ├── dataset.py
    │       └── baseline.py
    ├── data/
    │   ├── processed/
    │   │   └── daily_sales.csv
    │   └── raw/
    ├── notebooks/
    │   ├── raw_data_analysis.ipynb
    │   ├── clean_data_analysis.ipynb
    │   └── forecasting_analysis.ipynb
    ├── scripts/
    │   └── clean_data.py
    ├── .gitattributes
    ├── .gitignore
    ├── README.md
    └── requirements.txt

## Installation

### Requirements

- Python 3.14

Create a virtual environment from the project root:

    python -m venv .venv

Activate the virtual environment:

    .venv\Scripts\activate

or in PowerShell:

    .\.venv\Scripts\Activate.ps1

Install the project dependencies:

    python -m pip install -r requirements.txt

## Usage

### Running Analysis Scripts

The project contains numbered Python analysis scripts in the `analysis/` directory. These scripts are retained as the earlier script-based analysis workflow and can be executed individually from the project root through the terminal.

For example:

    python -m analysis.08_evaluate_baseline

    python -m analysis.09_profile_demand

### Data Cleaning

The data-cleaning pipeline is implemented in:

    scripts/clean_data.py

Run it from the project root through the terminal:

    python scripts/clean_data.py

The processed dataset will be written to:

    data/processed/daily_sales.csv

### JupyterLab

The primary interface for the current analysis is JupyterLab.

From the StockWise project root, start JupyterLab through the terminal:

    jupyter lab

or:

    python -m jupyter lab

JupyterLab will open in the browser. Navigate to the `notebooks/` directory and open one of the analysis notebooks:

    notebooks/
    ├── raw_data_analysis.ipynb
    ├── clean_data_analysis.ipynb
    └── forecasting_analysis.ipynb

The notebooks contain the current exploratory analysis, data validation, demand profiling, and forecasting experiments.

The notebooks should be opened from the project environment so that imports from `core/` and access to the project data directories work correctly.

## Privacy and Data Handling

The original UCI Online Retail dataset is not included in version control.

The `data/raw/` directory is excluded from the repository because the project does not redistribute the original dataset.

Any synthetic inventory data introduced later in the project will be clearly identified as synthetic.

## Limitations

The current project has several important limitations:

- The source dataset represents a UK-based online retailer rather than the fictional Examplemarkt business case used to demonstrate the project.
- The source dataset is transaction-oriented and does not provide a complete inventory-management data model.
- Actual inventory levels are not provided by the source dataset.
- Supplier lead times are not provided.
- Safety-stock parameters are not provided.
- Returns, damages, cancellations, and other inventory movements cannot always be reliably distinguished from the available fields.
- Cancellation records cannot always be reliably linked to their original orders, even when matching transaction attributes provide strong evidence of a relationship.
- The forecasting dataset contains highly intermittent demand.
- Some products have very limited historical observations.
- Extreme demand observations may strongly influence forecasting metrics.
- Positive-quantity transactions with zero unit prices have been investigated, but their treatment has not yet been formalised in the production cleaning pipeline.
- The final forecasting model has not yet been selected.
- Reorder recommendations will require additional inventory parameters that may need to be synthetically generated.

These limitations are part of the project's design and will be documented as the system develops.

## Future Improvements

Planned next steps include:

- Develop forecasting features.
- Evaluate additional statistical forecasting methods.
- Evaluate intermittent-demand forecasting methods such as Croston, SBA, and TSB.
- Train and evaluate machine-learning forecasting models.
- Compare statistical and machine-learning forecasting performance.
- Investigate product-level model selection.
- Investigate anomaly detection for unusual demand patterns.
- Introduce synthetic inventory levels and supplier lead times.
- Implement reorder-point and reorder-quantity calculations.

## License

The project uses the UCI Online Retail dataset, which is licensed under CC BY 4.0.

Dataset attribution:

    Chen, D. (2015). Online Retail. UCI Machine Learning Repository.

Dataset DOI:

    https://doi.org/10.24432/C5BW33
