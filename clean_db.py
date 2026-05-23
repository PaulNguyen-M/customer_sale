# ============================================
# CUSTOMER ANALYTICS DATA CLEANING PIPELINE
# File: DB.xlsx
# Sheet: FILE_DATA_HANDONLAB2
# ============================================

import pandas as pd
import numpy as np

# ============================================
# 1. LOAD DATASET
# ============================================

print("\n[1] Loading dataset...")

file_path = "./db/DB.xlsx"

df_raw = pd.read_excel(
    file_path,
    sheet_name="FILE_DATA_HANDONLAB2"
)

print(f"    → Dataset loaded successfully")
print(f"    → Shape: {df_raw.shape}")

# ============================================
# 2. CLEAN DATA
# ============================================

print("\n[2] Cleaning data...")

# --------------------------------------------
# 2.1 Remove completely empty rows
# --------------------------------------------

before_rows = len(df_raw)

df_raw.dropna(
    how='all',
    inplace=True
)

after_rows = len(df_raw)

print(f"    → Removed {before_rows - after_rows} empty rows")

# --------------------------------------------
# 2.2 Remove duplicate records
# --------------------------------------------

duplicate_count = df_raw.duplicated().sum()

df_raw.drop_duplicates(
    inplace=True
)

print(f"    → Removed {duplicate_count} duplicate rows")

# --------------------------------------------
# 2.3 Trim whitespace from text columns
# --------------------------------------------

text_cols = df_raw.select_dtypes(
    include=['object']
).columns

for col in text_cols:

    df_raw[col] = (
        df_raw[col]
        .astype(str)
        .str.strip()
    )

print(f"    → Standardized {len(text_cols)} text columns")

# --------------------------------------------
# 2.4 Convert numeric columns
# --------------------------------------------

numeric_columns = [
    'Revenue',
    'Unit Cost',
    'Unit Sale Price',
    'Income',
    'Customer Lifetime Value',
    'Quantity Sold',
    'Latitude',
    'Longitude'
]

for col in numeric_columns:

    if col in df_raw.columns:

        df_raw[col] = pd.to_numeric(
            df_raw[col],
            errors='coerce'
        )

print(f"    → Converted numeric columns")

# --------------------------------------------
# 2.5 Handle missing values
# --------------------------------------------

# Fill numeric nulls with median
for col in numeric_columns:

    if col in df_raw.columns:

        median_value = df_raw[col].median()

        df_raw[col] = df_raw[col].fillna(
            median_value
        )

# Fill text nulls
for col in text_cols:

    df_raw[col] = df_raw[col].replace(
        ['nan', 'None'],
        np.nan
    )

    df_raw[col] = df_raw[col].fillna(
        'Unknown'
    )

print(f"    → Missing values handled")

# ============================================
# 3. STANDARDIZE TEXT DATA
# ============================================

print("\n[3] Standardizing text data...")

columns_to_standardize = [
    'Gender',
    'Education',
    'Marital Status',
    'Country',
    'Province or State',
    'Product Line',
    'LoyaltyStatus'
]

for col in columns_to_standardize:

    if col in df_raw.columns:

        df_raw[col] = (
            df_raw[col]
            .astype(str)
            .str.title()
        )

print(f"    → Text formatting standardized")

# ============================================
# 4. FIX INCONSISTENT GENDER VALUES
# ============================================

print("\n[4] Fixing inconsistent gender values...")

if (
    'Loyalty#' in df_raw.columns and
    'Gender' in df_raw.columns
):

    gender_mode = (
        df_raw
        .groupby('Loyalty#')['Gender']
        .agg(lambda x: x.mode()[0])
    )

    df_raw['Gender'] = (
        df_raw['Loyalty#']
        .map(gender_mode)
    )

    print(f"    → Gender inconsistencies fixed")

# ============================================
# 5. CONVERT DATETIME
# ============================================

print("\n[5] Parsing datetime columns...")

date_columns = [
    'Order Date'
]

for col in date_columns:

    if col in df_raw.columns:

        df_raw[col] = pd.to_datetime(
            df_raw[col],
            errors='coerce'
        )

        print(
            f"    → {col} parsed successfully"
        )

# ============================================
# 6. FEATURE ENGINEERING
# ============================================

print("\n[6] Building analytical features...")

# --------------------------------------------
# 6.1 Revenue Validation
# --------------------------------------------

if all(
    col in df_raw.columns
    for col in [
        'Quantity Sold',
        'Unit Sale Price'
    ]
):

    df_raw['Calculated Revenue'] = (
        df_raw['Quantity Sold']
        *
        df_raw['Unit Sale Price']
    )

# --------------------------------------------
# 6.2 Total Cost
# --------------------------------------------

if all(
    col in df_raw.columns
    for col in [
        'Quantity Sold',
        'Unit Cost'
    ]
):

    df_raw['Total Cost'] = (
        df_raw['Quantity Sold']
        *
        df_raw['Unit Cost']
    )

# --------------------------------------------
# 6.3 Profit
# --------------------------------------------

if all(
    col in df_raw.columns
    for col in [
        'Revenue',
        'Total Cost'
    ]
):

    df_raw['Profit'] = (
        df_raw['Revenue']
        -
        df_raw['Total Cost']
    )

# --------------------------------------------
# 6.4 Profit Margin
# --------------------------------------------

if all(
    col in df_raw.columns
    for col in [
        'Profit',
        'Revenue'
    ]
):

    df_raw['Profit Margin (%)'] = np.where(
        df_raw['Revenue'] != 0,

        (
            df_raw['Profit']
            /
            df_raw['Revenue']
        ) * 100,

        0
    )

# --------------------------------------------
# 6.5 Extract Year / Month
# --------------------------------------------

if 'Order Date' in df_raw.columns:

    df_raw['Year'] = (
        df_raw['Order Date']
        .dt.year
    )

    df_raw['Month'] = (
        df_raw['Order Date']
        .dt.month
    )

# ============================================
# 7. DETECT OUTLIERS
# ============================================

print("\n[7] Detecting outliers...")

outlier_columns = [
    'Revenue',
    'Quantity Sold',
    'Customer Lifetime Value'
]

for col in outlier_columns:

    if col in df_raw.columns:

        Q1 = df_raw[col].quantile(0.25)
        Q3 = df_raw[col].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = (
            Q1 - (1.5 * IQR)
        )

        upper_bound = (
            Q3 + (1.5 * IQR)
        )

        df_raw[f'{col}_Outlier'] = np.where(

            (
                df_raw[col] < lower_bound
            ) |
            (
                df_raw[col] > upper_bound
            ),

            'Yes',
            'No'
        )

print(f"    → Outlier detection completed")

# ============================================
# 8. REMOVE INVALID VALUES
# ============================================

print("\n[8] Removing invalid values...")

# Remove negative revenue
if 'Revenue' in df_raw.columns:

    df_raw = df_raw[
        df_raw['Revenue'] >= 0
    ]

# Remove invalid quantity
if 'Quantity Sold' in df_raw.columns:

    df_raw = df_raw[
        df_raw['Quantity Sold'] > 0
    ]

# Remove negative unit cost
if 'Unit Cost' in df_raw.columns:

    df_raw = df_raw[
        df_raw['Unit Cost'] >= 0
    ]

df_raw.reset_index(
    drop=True,
    inplace=True
)

print(f"    → Invalid records removed")

# ============================================
# 9. FINAL DATA VALIDATION
# ============================================

print("\n[9] Final validation...")

print(f"    → Final Shape: {df_raw.shape}")

print(
    f"    → Missing values remaining:\n"
)

print(
    df_raw.isnull().sum()
)

# ============================================
# 10. EXPORT CLEANED DATA
# ============================================

print("\n[10] Exporting cleaned dataset...")

output_file = "Cleaned_data.xlsx"

df_raw.to_excel(
    output_file,
    index=False
)

print("\n====================================")
print("DATA CLEANING PIPELINE COMPLETED")
print("====================================")

print(f"Cleaned file saved as: {output_file}")
print(f"Final dataset shape: {df_raw.shape}")