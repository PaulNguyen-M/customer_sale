import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

import matplotlib.pyplot as plt
# ============================================
# LOAD DATA
# ============================================

print("\n[1] Loading dataset...")

file_path = "./db/DB.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="FILE_DATA_HANDONLAB2"
)

print(df.head())

print(f"    → Dataset loaded successfully")

# ==========================================
# DATA CLEANING
# ==========================================

print("\n[2] Cleaning data...")

df = df.drop_duplicates()

if 'Column1' in df.columns:
    df = df.drop(columns=['Column1'])

numeric_cols = [
    'Quantity Sold',
    'Unit Sale Price',
    'Unit Cost',
    'Revenue',
    'Customer Lifetime Value',
    'MonthsAsMember',
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median())

print(f"    → Data cleaning completed successfully")

# ==========================================
# FEATURE ENGINEERING
# ==========================================

print("\n[3] Feature engineering...")

df['Profit'] = ((df['Unit Sale Price'] - df['Unit Cost']) * df['Quantity Sold'])

df['AOV'] = df['Revenue'] / df['Quantity Sold']

print(f"    → Feature engineering completed successfully")

# ==========================================
# CUSTOMER LEVEL DATASET
# ==========================================

print("\n[4] Creating customer-level dataset...")

customer_df = df.groupby('Customer Name').agg({
    'Revenue': 'sum',
    'Profit': 'sum',
    'Quantity Sold': 'sum',
    'Customer Lifetime Value': 'mean',
    'MonthsAsMember': 'max'
}).reset_index()

customer_df.columns = [
    'Customer',
    'Monetary',
    'Profit',
    'Frequency',
    'CLV',
    'Recency'
]

print(customer_df.head())
print(f"    → Customer-level dataset created successfully")

# ==========================================
# SCALE DATA
# ==========================================

print("\n[5] Scaling data...")

features = ['Monetary', 'Profit', 'Frequency', 'CLV', 'Recency']
scaler = StandardScaler()
scaled_data = scaler.fit_transform(customer_df[features])
print(f"    → Data scaling completed successfully")

# ==========================================
# KMEANS CLUSTERING
# ==========================================
print("\n[6] Performing KMeans clustering...")

kmeans = KMeans(n_clusters=4, random_state=42)
customer_df['Cluster'] = kmeans.fit_predict(scaled_data)
print(customer_df.head())
print(f"    → KMeans clustering completed successfully")

# ==========================================
# VISUALIZATION
# ==========================================

print("\n[7] Visualizing clusters...")

plt.figure(figsize=(10, 6))

plt.scatter(
    customer_df['Monetary'],
    customer_df['Frequency'],
    c=customer_df['Cluster'],
)

plt.xlabel('Monetary')
plt.ylabel('Frequency')
plt.title('Customer Segments')

plt.show()

print(f"    → Visualization completed successfully")

# ==========================================
# DEFINE CHURN
# ==========================================

print("\n[8] Defining churn...")
# ==========================================
# DEFINE CHURN
# ==========================================

customer_df['Churn'] = np.where(

    (
        (customer_df['Frequency'] <= 2)
        &
        (customer_df['Monetary'] < customer_df['Monetary'].median())
    ),

    1,

    0
)

# ==========================================
# MACHINE LEARNING
# ==========================================

print("\n[9] Building machine learning model...")

X = customer_df[[
    'Monetary',
    'Profit',
    'Frequency',
    'CLV',
    'Recency'
]]


y = customer_df['Churn']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# ==========================================
# CHURN PROBABILITY
# ==========================================

print("\n[10] Calculating churn probability...")

customer_df['Churn_Probability'] = (
    model.predict_proba(X)[:,1]
)

# ==========================================
# RISK LEVEL
# ==========================================

print("\n[11] Assigning risk levels...")

def risk_level(prob):

    if prob >= 0.8:
        return 'Khẩn cấp'

    elif prob >= 0.6:
        return 'Cao'

    elif prob >= 0.4:
        return 'Trung bình'

    return 'Thấp'

customer_df['Risk_Level'] = (
    customer_df['Churn_Probability']
    .apply(risk_level)
)

# ==========================================
# ACTION RULE
# ==========================================

print("\n[12] Defining action rules...")

def action_rule(row):

    if row['Risk_Level'] == 'Khẩn cấp':
        return 'Gọi chăm sóc ngay'

    elif row['Risk_Level'] == 'Cao':
        return 'Gửi coupon ưu đãi'

    elif row['Risk_Level'] == 'Trung bình':
        return 'Theo dõi thêm'

    return 'Chăm sóc định kỳ'

customer_df['Action'] = customer_df.apply(
    action_rule,
    axis=1
)

# ==========================================
# EXPORT RESULT
# ==========================================

print("\n[13] Exporting results...")

customer_df.to_excel(
    'customer_segmentation_result.xlsx',
    index=False
)

print('Export Success!')

# ==========================================
# SUMMARY
# ==========================================
print("\n[14] Cluster summary...")

print('\nCluster Summary')

print(
    customer_df.groupby('Cluster')[
        ['Monetary', 'Frequency', 'CLV']
    ].mean()
)