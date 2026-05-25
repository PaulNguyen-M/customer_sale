# Customer Analytics & Churn Prediction System

> Hệ thống phân tích khách hàng, phân nhóm khách hàng và dự đoán churn nhằm hỗ trợ doanh nghiệp theo dõi hành vi khách hàng, tối ưu chiến lược retention và ra quyết định kinh doanh dựa trên dữ liệu.


# Tổng Quan Dự Án

Dự án được xây dựng nhằm giải quyết các bài toán:

* phân tích hành vi khách hàng
* theo dõi hiệu suất kinh doanh
* phân nhóm khách hàng bằng Machine Learning
* dự đoán khách hàng có nguy cơ churn
* hỗ trợ Sales ưu tiên chăm sóc khách hàng
* trực quan hóa dữ liệu bằng Dashboard

Toàn bộ pipeline được triển khai theo flow thực tế của Data Analyst & Machine Learning:

```text
Raw Data
→ Data Cleaning
→ Feature Engineering
→ Customer Segmentation
→ Churn Prediction
→ Dashboard Visualization
→ Business Insight
→ Business Recommendation
```


# Machine Learning Pipeline

## 1. KMeans Clustering

### Mục tiêu

Mô hình KMeans được sử dụng để:

* phân nhóm khách hàng
* xác định khách hàng VIP
* phát hiện khách hàng có nguy cơ churn
* hỗ trợ customer segmentation
* phục vụ chiến lược marketing

### Feature sử dụng

* Monetary
* Profit
* Frequency
* Customer Lifetime Value (CLV)

### Output

| Cluster   | Ý nghĩa                  |
| --------- | ------------------------ |
| Cluster 0 | Khách hàng VIP           |
| Cluster 1 | Khách hàng tiềm năng     |
| Cluster 2 | Khách hàng nguy cơ churn |
| Cluster 3 | Khách hàng mới           |


## 2. Logistic Regression

### Mục tiêu

Model Logistic Regression được sử dụng để:

* dự đoán churn customer
* tính xác suất khách hàng rời bỏ
* hỗ trợ retention strategy
* ưu tiên khách hàng cần chăm sóc

### Output

* Churn Probability
* Risk Level
* Action Recommendation

### Risk Level

| Risk Level | Ý nghĩa           |
| ---------- | ----------------- |
| Thấp       | Khách ổn định     |
| Trung bình | Cần theo dõi      |
| Cao        | Có nguy cơ churn  |
| Khẩn cấp   | Cần chăm sóc ngay |


# Công Nghệ & Công Cụ Sử Dụng

| Công nghệ    | Mục đích              |
| ------------ | --------------------- |
| Python       | Data Processing       |
| Pandas       | Data Cleaning         |
| NumPy        | Numerical Processing  |
| Scikit-learn | Machine Learning      |
| Matplotlib   | Visualization         |
| Seaborn      | Data Visualization    |
| Excel        | Dashboard & Reporting |
| GitHub       | Source Control        |


# Dataset

Dataset bao gồm:

* Customer Name
* Country
* City
* Product Line
* Revenue
* Profit
* Quantity Sold
* Customer Lifetime Value
* Loyalty Status
* Coupon Response

### Thông tin tổng quan

* dữ liệu khách hàng
* dữ liệu giao dịch
* dữ liệu doanh thu
* dữ liệu lợi nhuận
* dữ liệu loyalty
* dữ liệu hành vi mua hàng


# Quy Trình Làm Sạch Dữ Liệu

Dữ liệu gốc được xử lý bằng Python tại file:

```text
clean_db.py
```

## Pipeline xử lý bao gồm:

* remove duplicate
* xử lý missing values
* chuẩn hóa dữ liệu
* convert datatype
* feature engineering
* detect outliers


# Feature Engineering

Các feature được xây dựng:

* Monetary
* Profit
* Frequency
* Customer Lifetime Value
* Churn Probability
* Risk Level

### Ý nghĩa business

| Feature   | Ý nghĩa                     |
| --------- | --------------------------- |
| Monetary  | Tổng giá trị khách hàng     |
| Profit    | Lợi nhuận tạo ra            |
| Frequency | Tần suất mua hàng           |
| CLV       | Giá trị vòng đời khách hàng |


# Dashboard & Visualization

## 1. Customer Dashboard

Dashboard khách hàng hỗ trợ doanh nghiệp theo dõi:

* tổng doanh thu khách hàng
* customer segmentation
* churn probability
* loyalty status
* doanh thu theo quốc gia
* CLV theo customer group
* phân bố khách hàng theo giới tính và học vấn

### Dashboard Path

```text
./img/customer_dashboard.png
```

![Customer Dashboard](./img/customer_dashboard.png)

### KPI Chính

* Tổng khách hàng
* Tổng doanh thu
* Tổng lợi nhuận
* Average CLV
* Profit Margin
* Churn Risk Customer

### Giá trị doanh nghiệp

Dashboard giúp doanh nghiệp:

* xác định khách hàng giá trị cao
* phát hiện khách hàng nguy cơ churn
* tối ưu retention strategy
* theo dõi loyalty program
* tăng customer lifetime value
* hỗ trợ data-driven decision making

---

## 2. Product Dashboard

Dashboard sản phẩm hỗ trợ theo dõi:

* doanh thu theo dòng sản phẩm
* lợi nhuận theo sản phẩm
* top sản phẩm bán chạy
* hiệu suất sản phẩm theo thời gian
* tỷ lệ đóng góp doanh thu
* phân tích margin theo sản phẩm

### Dashboard Path

```text
./img/product_dashboard.png
```

![Product Dashboard](./img/product_dashboard.png)

### KPI Chính

* Revenue
* Profit
* Quantity Sold
* Profit Margin
* Top Product
* Product Performance

### Giá trị doanh nghiệp

Dashboard giúp doanh nghiệp:

* xác định sản phẩm chiến lược
* tối ưu marketing campaign
* tối ưu inventory
* phát hiện sản phẩm hiệu suất thấp
* tối ưu doanh thu và lợi nhuận


# Business Insight

## 1. Customer Insight

### High Value Customer

* nhóm khách hàng VIP tạo ra phần lớn doanh thu
* khách hàng loyalty cao có CLV lớn
* nhóm khách hàng trung thành có tần suất mua ổn định

### Churn Customer

* nhóm churn có frequency thấp
* churn customer thường có doanh thu thấp
* nhiều khách hàng churn không tham gia loyalty program

### Business Impact

Nếu không giữ chân nhóm khách hàng churn:

* doanh thu dài hạn sẽ giảm
* tăng chi phí marketing acquisition
* giảm customer retention rate

### Strategic Recommendation

* triển khai personalized offer
* ưu tiên chăm sóc nhóm churn risk cao
* xây dựng loyalty program nhiều tầng
* tăng retention cho nhóm CLV cao


## 2. Product Insight

### Revenue Driver

* một số product line đóng góp phần lớn doanh thu
* nhóm sản phẩm high-margin ảnh hưởng mạnh đến lợi nhuận

### Product Performance

* tồn tại sản phẩm doanh thu cao nhưng margin thấp
* một số product line giảm hiệu suất theo thời gian

### Strategic Recommendation

* tập trung marketing cho high-margin products
* tối ưu cross-selling
* giảm tồn kho sản phẩm hiệu suất thấp
* xây dựng combo/bundle sản phẩm


# Output Sau Khi Chạy ML

## File Export

```text
customer_segmentation_result.xlsx
```

### Bao gồm:

* Customer
* Monetary
* Profit
* Frequency
* CLV
* Cluster
* Churn Probability
* Risk Level
* Action


# Cấu Trúc Thư Mục

```text
CUSTOMER_SALES/
│
├── db/
│   └── DB.xlsx
│
├── img/
│   ├── customer_dashboard.png
│   └── product_dashboard.png
│
├── customer_segmentation_result.xlsx
│
├── churn_pipeline_ml.py
├── clean_db.py
├── requirements.txt
└── README.md
```


# requirements.txt

```txt
pandas==2.2.2
numpy==1.26.4
openpyxl==3.1.5

scikit-learn==1.5.1
xgboost==2.1.1

matplotlib==3.9.2
seaborn==0.13.2
```


# Hướng Dẫn Chạy Project

## 1. Clone Repository

```bash
git clone <your-repository>
```


## 2. Cài Đặt Thư Viện

```bash
pip install -r requirements.txt
```


## 3. Chạy Pipeline Làm Sạch Dữ Liệu

```bash
python clean_db.py
```

### Output

```text
Cleaned_data.xlsx
```


## 4. Chạy Machine Learning Pipeline

```bash
python churn_pipeline_ml.py
```

### Output

```text
customer_segmentation_result.xlsx
```


# Giá Trị Mang Lại

Hệ thống hỗ trợ:

* customer analytics
* customer segmentation
* churn prediction
* retention strategy
* business reporting
* dashboard analytics
* data-driven decision making


# Executive Summary

Hệ thống Customer Analytics & Churn Prediction giúp doanh nghiệp chuyển đổi dữ liệu giao dịch thành hệ thống phân tích khách hàng thông minh.

Thông qua Dashboard Analytics và Machine Learning, doanh nghiệp có thể:

* hiểu rõ hành vi khách hàng
* dự đoán nguy cơ churn
* tối ưu chiến lược retention
* tăng customer lifetime value
* tối ưu doanh thu và lợi nhuận
* hỗ trợ ra quyết định kinh doanh dựa trên dữ liệu

Dự án được triển khai theo hướng thực tế của một Data Analyst kết hợp Machine Learning Analytics nhằm mô phỏng quy trình phân tích dữ liệu trong doanh nghiệp hiện đại.
