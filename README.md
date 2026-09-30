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

Negative transactions were investigated to distinguish customer cancellations from other inventory-related adjustments.

The analysis showed that negative quantities do not represent cancellations exclusively. Some records represent operational events such as:

- *"thrown away"*
- *"Unsaleable, destroyed"*
- *"damages"*
- *"damaged"*
- *"Manual"*
- *"check"*
- missing or unclear descriptions

For the initial forecasting dataset, observable demand is defined as positive transaction quantity.

Current transaction classification:

| Transaction Type     | Identification                                   | Used for Demand Forecasting
|----------------------|--------------------------------------------------|----------------------------
| Sale                 | "Quantity" > 0                                   | Yes
| Cancellation         | "InvoiceNo" starts with  C                       | No 
| Inventory adjustment | Negative quantity without a cancellation invoice | No

The initial data-processing workflow is:

    Online Retail.xlsx

    Data Quality Analysis

    Transaction Classification

            Sales
            Cancellations
            Inventory Adjustments

    Positive Sales Transactions

    Daily Product Demand

Initial analysis and processing scripts are located in:

    scripts/

Current scripts include:

    scripts/inspect_data.py
    scripts/data_quality.py
    scripts/clean_data.py

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