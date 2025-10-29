import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import os
import sqlite3
from datetime import datetime, timedelta

# -----------------------------------------------------------
# 🗂️ Folder Setup
# -----------------------------------------------------------
os.makedirs("data", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# -----------------------------------------------------------
# 🧮 Generate Synthetic Retail Dataset
# -----------------------------------------------------------
regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Clothing", "Furniture", "Grocery", "Sports"]
payment_modes = ["Credit Card", "Cash", "UPI", "Debit Card", "Net Banking"]
product_names = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Camera"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Dress", "Shoes"],
    "Furniture": ["Office Chair", "Sofa", "Table", "Bed", "Cupboard"],
    "Grocery": ["Rice Bag", "Wheat Flour", "Oil", "Snacks", "Biscuits"],
    "Sports": ["Football", "Cricket Bat", "Tennis Racket", "Gym Gloves", "Yoga Mat"]
}

np.random.seed(42)
rows = 1000
data = []

for i in range(rows):
    order_id = f"ORD{i+1:04d}"
    date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 273))
    region = random.choice(regions)
    category = random.choice(categories)
    product = random.choice(product_names[category])
    quantity = random.randint(1, 5)
    unit_price = random.randint(200, 8000)
    total_sales = quantity * unit_price
    profit = round(total_sales * random.uniform(0.1, 0.25), 2)
    payment = random.choice(payment_modes)
    customer_name = random.choice(["Aarav", "Diya", "Arjun", "Riya", "Ishaan", "Meera", "Vivaan", "Ananya"]) + " " + random.choice(["Patel", "Sharma", "Mehta", "Rao", "Singh", "Das"])
    data.append([order_id, date, customer_name, region, category, product, quantity, unit_price, total_sales, profit, payment])

columns = ["Order_ID", "Order_Date", "Customer_Name", "Region", "Product_Category", "Product_Name", "Quantity", "Unit_Price", "Total_Sales", "Profit", "Payment_Mode"]
df = pd.DataFrame(data, columns=columns)

# -----------------------------------------------------------
# 💾 Save Dataset to CSV & Excel
# -----------------------------------------------------------
csv_path = "data/retail_sales_data.csv"
excel_path = "data/retail_sales_data.xlsx"
df.to_csv(csv_path, index=False)
df.to_excel(excel_path, index=False)

print("✅ Dataset created successfully!")
print(f"CSV File: {csv_path}")
print(f"Excel File: {excel_path}")

# -----------------------------------------------------------
# 🧠 Load Data into SQLite Database
# -----------------------------------------------------------
conn = sqlite3.connect("data/retail_sales.db")
df.to_sql("retail_sales", conn, if_exists="replace", index=False)
print("✅ Data successfully loaded into SQLite database!\n")

# -----------------------------------------------------------
# 🧾 SQL Queries for Analysis
# -----------------------------------------------------------
queries = {
    "1️⃣ Total Sales by Region": """
        SELECT Region, SUM(Total_Sales) AS Total_Sales
        FROM retail_sales
        GROUP BY Region
        ORDER BY Total_Sales DESC;
    """,
    "2️⃣ Average Profit by Category": """
        SELECT Product_Category, ROUND(AVG(Profit),2) AS Avg_Profit
        FROM retail_sales
        GROUP BY Product_Category
        ORDER BY Avg_Profit DESC;
    """,
    "3️⃣ Top 5 Customers by Sales": """
        SELECT Customer_Name, SUM(Total_Sales) AS Total_Sales
        FROM retail_sales
        GROUP BY Customer_Name
        ORDER BY Total_Sales DESC
        LIMIT 5;
    """,
    "4️⃣ Total Orders by Payment Mode": """
        SELECT Payment_Mode, COUNT(Order_ID) AS Total_Orders
        FROM retail_sales
        GROUP BY Payment_Mode;
    """,
    "5️⃣ Monthly Sales Trend": """
        SELECT strftime('%Y-%m', Order_Date) AS Month, SUM(Total_Sales) AS Monthly_Sales
        FROM retail_sales
        GROUP BY Month
        ORDER BY Month;
    """
}

for title, query in queries.items():
    print(f"\n🔹 {title}")
    result = pd.read_sql_query(query, conn)
    print(result)

# -----------------------------------------------------------
# 📊 Charts Visualization
# -----------------------------------------------------------
# 1️⃣ Sales by Region
plt.figure(figsize=(7, 4))
sales_by_region = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
sales_by_region.plot(kind="bar", color="skyblue")
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("charts/sales_by_region.png")
plt.show()

# 2️⃣ Profit by Product Category
plt.figure(figsize=(7, 4))
profit_by_category = df.groupby("Product_Category")["Profit"].sum().sort_values(ascending=False)
profit_by_category.plot(kind="barh", color="orange")
plt.title("Profit by Product Category")
plt.xlabel("Profit")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig("charts/profit_by_category.png")
plt.show()

# 3️⃣ Monthly Sales Trend
plt.figure(figsize=(8, 4))
df["Month"] = pd.to_datetime(df["Order_Date"]).dt.to_period("M")
monthly_sales = df.groupby("Month")["Total_Sales"].sum()
monthly_sales.plot(kind="line", marker="o", color="green")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png")
plt.show()

# 4️⃣ Payment Mode Distribution
plt.figure(figsize=(6, 6))
payment_counts = df["Payment_Mode"].value_counts()
payment_counts.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Payment Mode Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/payment_mode_distribution.png")
plt.show()

# 5️⃣ Top 10 Customers by Total Sales
plt.figure(figsize=(8, 4))
top_customers = df.groupby("Customer_Name")["Total_Sales"].sum().sort_values(ascending=False).head(10)
top_customers.plot(kind="bar", color="purple")
plt.title("Top 10 Customers by Total Sales")
plt.xlabel("Customer Name")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("charts/top_10_customers.png")
plt.show()

print("\n✅ All SQL analyses and visual charts generated successfully!")
conn.close()

