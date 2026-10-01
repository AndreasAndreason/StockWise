# StockWise — Inventory Demand Forecasting & Reorder Recommendation System

An independent Python project that explores inventory demand forecasting and inventory reorder recommendations using historical transaction data.

## Overview

The project uses historical retail transaction data to explore how data analysis, machine learning, and inventory management logic can be combined to support better stock planning.

The planned system will:

- Analyze historical product sales
- Forecast future product demand
- Identify products that may require replenishment
- Calculate reorder recommendations based on forecast demand and inventory parameters
- Detect unusual sales patterns
- Present key inventory metrics through a dashboard

### Data Source

This project uses the Online Retail dataset provided by the UCI Machine Learning Repository for demonstrative purposes.

**Dataset:** Chen, D. (2015). Online Retail.

UCI Machine Learning Repository.

**DOI:** https://doi.org/10.24432/C5BW33

**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The original dataset contains transaction data from a UK-based online retailer. It is used as a source of data for developing and demonstrating StockWise.

The original dataset is not included in this repository.
The *data/raw/* directory is excluded from version control.

The source data is processed and transformed for this project. Inventory levels, supplier lead times, safety-stock parameters, and other business-specific data may be synthetically generated.

Changes made to the source data will be documented.

The dataset's authors and the UCI Machine Learning Repository are not affiliated with or endorsing this project.

## Project Status

**Status:** In Development

## Features

### Data

Initial analysis of the Online Retail dataset identified:

- 541,909 transaction lines
- 4,070 unique products
- 25,900 unique invoices
- Transaction dates from December 2010 to December 2011
- Missing product descriptions
- Missing "CustomerID" values
- 10,624 transactions with negative quantities
- 9,288 cancellation invoices

Negative transaction records were investigated to better understand their meaning and determine how they should be handled during demand-data preparation.

The investigation showed that negative quantities do not exclusively represent customer cancellations. Some records appear to describe operational events or inventory adjustments, including:

- *"thrown away"*
- *"Unsaleable, destroyed"*
- *"damages"*
- *"damaged"*
- *"Manual"*
- *"check"*
- missing or unclear descriptions

Consequently, negative quantities are not treated as a direct measure of customer returns or cancellations.

#### Transaction Classification

Transactions are classified using the available invoice numbers and quantity values:

| Transaction Type     | Identification                                   | Demand Treatment
|----------------------|--------------------------------------------------|------------------------------------------
| Sale                 | "Quantity" > 0                                   | Included unless matched to a cancellation
| Cancellation         | "InvoiceNo" starts with  "C"                     | Excluded from demand
| Inventory adjustment | Negative quantity without a cancellation invoice | Excluded from demand

#### Cancellation Matching

A further investigation identified cases where a positive sales line was subsequently reversed by a cancellation record. Simply aggregating all positive quantities would retain these reversed sales and could inflate measured demand.

The cleaning workflow therefore attempts to match cancellation lines to earlier sales lines. The current matching heuristic uses the following conditions:

- The product identifier (*"StockCode"*) must match.
- The unit price (*"UnitPrice"*) must match.
- The cancellation quantity must equal the absolute quantity of the candidate sale.
- The sale must occur before the cancellation.
- The time difference must not exceed 14 days.
- A positive sales line can be matched only once.

When a match is found, the corresponding positive sales line is excluded from the demand dataset.

The 14-day matching window is a project-specific heuristic informed by inspection of the transaction records. It does not represent a verified cancellation policy of the original retailer.

Matching is based on available transaction fields and cannot establish with certainty that two records refer to the same underlying order. Unmatched cancellation records do not automatically remove positive sales.

#### Demand Definition

For the initial forecasting dataset, demand is defined as the sum of positive sales quantities remaining after the cancellation-matching procedure.

Negative cancellation and inventory-adjustment records are not directly counted as demand. Positive sales lines matched to cancellations within the configured matching window are also excluded.

This approach aims to reduce identifiable reversals while preserving recorded sales that cannot be reliably matched to a cancellation.

#### Demand Investigation and Outlier Handling

After applying the cleaning workflow, the processed demand data was investigated to identify unusually large product-day quantities and high-volume sales dates.

The investigation highlighted a recorded demand quantity of **12,540 units** for product *"84826"* on **25 November 2011**.

The corresponding raw transactions were inspected. No cancellation was identified for this position, so the observation is retained in the processed dataset.

Although the quantity is substantially larger than other observed product-day values, its magnitude alone is not sufficient evidence that it is invalid. Removing it during data cleaning would risk discarding a genuine bulk sale.

The current approach is therefore to:

- Preserve the observation in the processed demand data.
- Investigate unusually large quantities rather than automatically deleting them.
- Evaluate statistical methods for identifying extreme demand values in a later stage.
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
            +------------------------+
            |                        |
            v                        v
       Sales Lines          Negative Transactions
            |                        |
            |                +-------+--------+
            |                |                |
            |                v                v
            |          Cancellations   Inventory Adjustments
            |                |
            +----------------+
                    |
                    v
         Cancellation Matching
          (14-day heuristic)
                    |
                    v
       Exclude Matched Sales Lines
                    |
                    v
        Aggregate Daily Demand
        by Date and StockCode
                    |
                    v
       data/processed/daily_sales.csv

Initial data analysis, investigation, and processing scripts are located in:

    scripts/

Current scripts include:

    scripts/inspect_data.py
    scripts/data_quality.py
    scripts/clean_data.py
    scripts/inspect_processed_data.py
    scripts/inspect_demand.py
    scripts/inspect_product.py
    scripts/inspect_cancellations.py

The scripts support raw-data inspection, data-quality checks, transaction classification, cancellation investigation, demand cleaning, and analysis of the processed dataset.

The processed demand dataset is generated at:

    data/processed/daily_sales.csv

### Data Model

The initial processed demand dataset contains:

|Field     | Description
|----------|-----------------------------------------------------------------
|Date      | Transaction date
|StockCode | Product identifier
|Demand	   | Total positive transaction quantity for the product on that date

The source transaction data also contains:

- Invoice number
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

Further data modelling will be developed as the project progresses.

#### Current Data Preparation Status

The initial data preparation stage focuses on understanding the source data and producing a daily product-demand dataset.

Completed work includes:

- Initial inspection of the raw transaction dataset.
- Analysis of missing values and negative quantities.
- Classification of sales, cancellations, and inventory adjustments.
- Investigation of cancellation-to-sale matching.
- Implementation of a configurable cancellation-matching window.
- Inspection of unusually large product-day demand values.
- Generation and validation of the processed daily-demand dataset.

The current output contains daily demand aggregated by date and product identifier. Further work will focus on demand analysis, feature engineering, and forecasting.

The cleaning logic is based on the fields available in the source dataset. Because the original retailer's operational rules are not fully documented, some transaction interpretations and matching decisions remain heuristic.

### Architecture



### Machine Learning



### API



### Dashboard



## Technology Stack

- Python 3.14
- pandas
- NumPy

## Application Workflow



## Project Structure

    StockWise/
        data/
            processed/
            raw/
        scripts/
            clean_data.py
            data_quality.py
            inspect_data.py
        .gitattributes
        .gitignore        
        README.md

## Installation

### Requirements

- Python 3.14.

## Usage

Initial data inspection:

    python scripts/inspect_data.py

Run the data-quality analysis:

    python scripts/data_quality.py

Generate the initial processed daily-demand dataset:

    python scripts/clean_data.py

The processed dataset will be written to:

    data/processed/daily_sales.csv

Further usage instructions will be added as the API, forecasting pipeline, and dashboard are implemented.

## Privacy and Data Handling



## Limitations



## Future Improvements

## License

The project uses the UCI Online Retail dataset, which is licensed under CC BY 4.0.

Dataset attribution:

    Chen, D. (2015). Online Retail. UCI Machine Learning Repository.

Dataset DOI:

    https://doi.org/10.24432/C5BW33