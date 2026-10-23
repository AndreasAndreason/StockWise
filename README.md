# StockWise — Inventory Demand Forecasting & Reorder Recommendation System

An independent Python project that explores inventory demand forecasting and inventory reorder recommendations using historical transaction data.

## Overview

The project uses historical retail transaction data to explore how data analysis, statistical forecasting, machine learning, and inventory management logic can be combined to support better stock planning.

The current focus is on:

- Analyzing historical product sales
- Cleaning and validating transaction data
- Building daily product-level demand series
- Evaluating demand forecasting baselines
- Profiling product-level demand characteristics
- Developing forecasting features and machine-learning models

Inventory reorder recommendations and other application functionality will be developed after the forecasting stage.

### Data Source

This project uses the Online Retail dataset provided by the UCI Machine Learning Repository for demonstrative purposes.

**Dataset:** Chen, D. (2015). Online Retail.

UCI Machine Learning Repository.

**DOI:** https://doi.org/10.24432/C5BW33

**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The original dataset contains transaction data from a UK-based online retailer. It is used as a source of data for developing and demonstrating StockWise.

The original dataset is not included in this repository.
The `data/raw/` directory is excluded from version control.

The source data is processed and transformed for this project. Inventory levels, supplier lead times, safety-stock parameters, and other business-specific data may be synthetically generated later.

The dataset's authors and the UCI Machine Learning Repository are not affiliated with or endorsing this project.

## Project Status

**Status:** In Development

The current development stage focuses on data preparation, demand analysis, forecasting baselines, and preparation for machine-learning forecasting.

## Features

### Data

StockWise intentionally deals with imperfect, poorly structured transactional data because this reflects a common real-world data-engineering problem in retail.

The source dataset was not designed as a normalized inventory-management database. It provides transaction-level records, but important business concepts such as sales, cancellations, returns, damages, and inventory adjustments are not represented as a complete explicit transaction model.

Consequently, part of the project involves interpreting the available fields, classifying transactions, investigating ambiguous records, and creating analytical datasets appropriate for specific use cases.

Initial analysis of the Online Retail dataset identified:

- 541,909 transaction lines
- 4,070 unique products
- 25,900 unique invoices
- Transaction dates from December 2010 to December 2011
- Missing product descriptions
- Missing `CustomerID` values
- 10,624 transactions with negative quantities
- 9,288 cancellation invoices

This data-quality investigation is an intentional part of the project. The goal is not simply to remove unusual records, but to determine what information can be reliably inferred from the source data without inventing business relationships that are not actually provided.

#### Transaction Classification

Transactions are classified using the available invoice numbers and quantity values:

| Transaction Type | Identification | Demand Treatment |
|------------------|----------------|------------------|
| Sale | `Quantity > 0` | Included |
| Cancellation | `InvoiceNo` starts with `C` | Excluded |
| Inventory adjustment | Negative quantity without a cancellation invoice | Excluded |

The UCI dataset documentation identifies invoice numbers beginning with `C` as cancellations.

Negative quantities are not automatically interpreted as customer returns. Investigation of the source data found negative records with descriptions such as:

- *"thrown away"*
- *"Unsaleable, destroyed."*
- *"damages"*
- *"damaged"*
- *"Manual"*
- *"check"*
- missing or unclear descriptions

These observations indicate that negative transactions can represent different operational events. The available source fields do not provide enough information to reliably distinguish every possible business meaning.

Therefore, StockWise preserves the distinction between cancellations and other negative transactions rather than treating all negative quantities as customer returns.

#### Cancellation Matching

An initial investigation attempted to match cancellation records to earlier positive sales.

The matching approach used:

- the same `StockCode`
- the same `UnitPrice`
- the same absolute `Quantity`
- an earlier `InvoiceDate`
- a limited time window
- one-to-one matching between cancellation and sale records

This investigation was useful for understanding the data, but it was ultimately rejected as part of the demand-cleaning process.

The source dataset identifies cancellation records but does not provide an explicit relationship or transaction ID linking a cancellation to its original order. Therefore, a statistical match based on product, quantity, price, and time cannot establish with certainty that two records represent the same underlying order.

Cancellation records are consequently treated as independent transaction events and excluded from the demand dataset rather than being used to remove potentially corresponding positive sales.

The previously investigated matching approach remains part of the project's data-quality investigation, but it is not used by the current cleaning logic.

#### Demand Definition

For the initial forecasting dataset, demand is defined as the sum of positive sales quantities.

Cancellation records and other negative inventory movements are not treated as negative demand.

The resulting `daily_sales.csv` dataset therefore represents historical product demand, rather than a complete representation of every physical inventory movement.

#### Demand Investigation and Outlier Handling

After the initial demand preparation, the processed demand data was investigated to identify unusually large product-day quantities and high-volume sales dates.

The investigation highlighted:

- A recorded demand quantity of 80,995 units for product `23843`
- A recorded demand quantity of 12,540 units for product `84826` on 25 November 2011
- Other high-volume product-day observations

The corresponding raw transactions were inspected where appropriate. The 12,540-unit observation for product `84826` did not have an identified cancellation at the investigated position and was therefore retained.

The 80,995-unit observation was also retained. Although it is an extreme observation, its magnitude alone is not sufficient evidence that it is invalid.

The current approach is therefore to:

- Preserve unusual observations in the processed demand data.
- Investigate unusually large quantities rather than automatically deleting them.
- Evaluate statistical methods for identifying extreme demand values.
- Report detected deviations transparently.
- Assess the impact of extreme observations on forecasting performance.

Outlier detection and treatment will be considered separately from transaction cleaning. Any future exclusion, transformation, or adjustment will be documented and evaluated against the original data.

#### Processing Workflow

The current data-processing workflow is:

    Online Retail.xlsx
           |
           v
    Data Quality Analysis
           |
           v
    Transaction Classification
           |
           +----------------------+
           |                      |
           v                      v
         Sales            Negative Transactions
           |               |                |
           |               v                v
           |        Cancellations   Inventory Adjustments
           |
           v
    Aggregate Daily Demand
    by Date and StockCode
           |
           v
    data/processed/daily_sales.csv

The project originally used numbered Python scripts for exploratory analysis and development.

The existing `analysis/` directory is intentionally retained as the historical script-based analysis work. It is not being removed as part of the notebook migration.

Further analytical development is now being performed in Jupyter notebooks.

The current notebook workflow is organized into:

    notebooks/
    ├── 01_raw_data_analysis.ipynb
    ├── 02_clean_data_analysis.ipynb
    └── 03_forecasting_analysis.ipynb

The notebooks are now the primary location for ongoing exploratory, validation, and forecasting analysis.

The existing analysis scripts remain available for reference:

    analysis/

The data-cleaning script is located in:

    scripts/

The main project runner is:

    stockwise.py

The analysis scripts are numbered chronologically and are preserved as the previous script-based analysis workflow.

Current analysis scripts include:

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

The cleaning script is:

    scripts/clean_data.py

The processed demand dataset is generated at:

    data/processed/daily_sales.csv

### Data Model

The initial processed demand dataset contains:

| Field | Description |
|-------|-------------|
| `Date` | Transaction date |
| `StockCode` | Product identifier |
| `Demand` | Total positive sales quantity for the product on that date |

The source transaction data also contains:

- Invoice number
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

Further data modelling will be developed as the project progresses.

### Current Data Preparation Status

The initial data preparation stage focuses on understanding the source data and producing a daily product-demand dataset.

Completed work includes:

- Initial inspection of the raw transaction dataset.
- Analysis of missing values and negative quantities.
- Classification of sales, cancellations, and inventory adjustments.
- Investigation of cancellation-to-sale matching.
- Rejection of unreliable cancellation-to-sale matching as part of demand cleaning.
- Definition of demand as positive sales quantities.
- Inspection of unusually large product-day demand values.
- Generation and validation of the processed daily-demand dataset.
- Separation of exploratory analysis from the operational data-cleaning script.
- Migration of ongoing analysis from numbered Python scripts to Jupyter notebooks.
- Creation of a continuous daily time series for each product within its observed activity period.
- Filling missing product-days within the observed activity period with zero demand.
- Evaluation of a 7-day seasonal-naive forecasting baseline.
- Statistical profiling of product-level demand characteristics.

The current output contains daily demand aggregated by date and product identifier.

The forecasting dataset currently contains:

- 3,941 products
- 1,077,874 product-day observations
- Date range from 2010-12-01 to 2011-12-09
- 801,031 zero-demand product-days
- 276,843 positive-demand product-days
- Approximately 74.4% zero-demand observations

### Demand Forecasting Analysis

The forecasting stage begins with statistical analysis before applying machine-learning models.

The purpose is to understand the structure of product demand and select forecasting methods based on the observed data characteristics rather than assuming that a single machine-learning model is appropriate for every product.

#### Continuous Product Time Series

The aggregated demand dataset contains only product-days on which transactions were recorded.

For forecasting, each product is converted into a continuous daily time series covering its observed activity period:

- The first observed sale defines the beginning of the product's activity period.
- The last observed sale defines the end of the activity period.
- Missing dates inside that period are added with `Demand = 0`.
- Dates before the first observed sale and after the last observed sale are not artificially filled.

This produces a forecasting dataset suitable for lag-based and time-series forecasting methods.

#### Baseline Forecast

The first forecasting benchmark is a 7-day seasonal-naive baseline:

    Forecast(t) = Demand(t - 7)

The model assumes that demand for a product on a given day will be equal to its demand seven days earlier.

Evaluation uses a chronological 80/20 time-based split rather than a random split.

The current evaluation produced:

| Metric | Result |
|--------|--------|
| Cutoff date | 2011-09-26 |
| Training rows | 843,845 |
| Test rows | 207,492 |
| MAE | 10.11 |
| RMSE | 62.37 |

The baseline is retained as a reference point for subsequent statistical and machine-learning forecasting methods.

#### Statistical Demand Profile

The product-level demand profile revealed several important characteristics.

Across the 3,941 products:

- Average active history: approximately 274 days
- Median active history: 353 days
- Average zero-demand percentage: approximately 70.5%
- Median zero-demand percentage: approximately 78.4%
- Average positive-demand percentage: approximately 29.5%
- Median positive-demand percentage: approximately 21.6%
- Average coefficient of variation: approximately 4.36
- Median coefficient of variation: approximately 3.75

The forecasting dataset therefore exhibits substantial intermittency.

Many products have zero demand on most observed days. Some products have extremely sparse demand; for example, product `79151B` has only two positive-demand days across 359 active days.

Demand is also highly skewed and variable. The difference between mean and median demand is substantial for many products, and some products contain very large individual demand events.

Examples include:

- Product `84826`: mean demand approximately 36.94 units, standard deviation approximately 651.14, maximum 12,540 units.
- Product `23166`: mean demand approximately 239.37 units, median demand 0, maximum 74,215 units.
- Product `23843`: one observed active day with demand of 80,995 units.

These results indicate that StockWise is not simply a conventional smooth demand-forecasting problem.

The data contains:

- Frequent zero-demand periods
- Intermittent demand
- High demand variability
- Strong right-skewness
- Extreme demand events
- Products with very different amounts of historical information

Because of these characteristics, the forecasting strategy will first evaluate statistical and intermittent-demand methods before relying on machine-learning models.

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

Models will be evaluated using chronological time-based validation.

Machine-learning models will be compared against the established statistical baselines rather than evaluated in isolation.

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

Activation in PowerShell:

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

JupyterLab will open in the browser. Navigate to the `notebooks/` directory and open one of the analysis notebooks:

    notebooks/
    ├── 01_raw_data_analysis.ipynb
    ├── 02_clean_data_analysis.ipynb
    └── 03_forecasting_analysis.ipynb

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
- Cancellation records cannot be reliably linked to their original orders.
- The forecasting dataset contains highly intermittent demand.
- Some products have very limited historical observations.
- Extreme demand observations may strongly influence forecasting metrics.
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