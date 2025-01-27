''' \

Here are three extremely hard Pandas problems that will help you level up your skills and prepare for a Google-level data science interview:

Problem 1: Multi-Level Time Series Aggregation with Missing Data
You are provided with a time-series dataset of e-commerce transactions with multiple products, categories, and user interactions.

Dataset columns:

date: The date of the transaction
user_id: Unique identifier for each user
product_id: Unique identifier for each product
category: The product category (e.g., "electronics", "clothing")
price: Price of the product
quantity: Quantity purchased
timestamp: Exact timestamp of the transaction (optional)
Task:

Create a time series of daily sales for each category, product, and user.
Compute the total sales (price * quantity) per product for each day.
Fill missing sales data for days where no transactions occurred, using the forward fill method, and then apply exponential moving average smoothing to the sales data.
Identify any unusual spikes in sales, where the sales for a product exceed the historical 90th percentile of that product's sales.
Visualize the trend for the top 3 products with the highest average sales per day.
\ 
'''


import pandas as pd
import numpy as np

np.random.seed(42)

n = 1000

date_range = pd.date_range(start="2023-01-01", end="2023-12-31", freq='h')
user_ids = np.random.randint(1, 100, n)
product_ids = np.random.randint(1, 50, n)
categories = np.random.choice(['electronics', 'clothing', 'groceries', 'furniture'], n)

prices = np.round(np.random.uniform(10, 500, n), 2)
quantities = np.random.randint(1, 10, n).astype(float)

quantity_missing_indices = np.random.choice(n, int(0.1 * n), replace=False)
quantities[quantity_missing_indices] = np.nan
timestamps = pd.to_datetime(np.random.choice(date_range, n))
df = pd.DataFrame({
    'date': np.random.choice(date_range, n),
    'user_id': user_ids,
    'product_id': product_ids,
    'category': categories,
    'price': prices,
    'quantity': quantities,
    'timestamp': timestamps
})

df = df.sort_values(by="date")
# solution 
df['date'] = pd.to_datetime(df['date'] ) 

df['daily_sales'] = df['price'] * df['quantity']

final_df = pd.DataFrame()
for (category,product_id,user_id) , group in df.groupby(['category','product_id','user_id']):

    min_date = group["date"].min()

    max_date = group["date"].max()
    
    date_range = pd.date_range(start = min_date , end = max_date , freq = "D")
    group.set_index(['date'],inplace = True)
    date_range_df = pd.DataFrame(date_range, columns = ["date"])
    date_range_df.set_index("date",inplace = True)
    date_range_df["category"] = category
    date_range_df["product_id"] = product_id 
    date_range_df["user_id"] = user_id 
    
    merge_data = date_range_df.merge(group[['daily_sales','price','quantity']],left_index= True,right_index = True, how = "left")
    
    merge_data["daily_sales"] = merge_data['daily_sales'].fillna(method = "bfill")
    merge_data['daily_sales'] = merge_data['daily_sales'].fillna(method = 'ffill')
    
    final_df = pd.concat([final_df,merge_data])

df = final_df.reset_index()

print(df)
df['total_sales'] = df['price'] * df['quantity']
df = df.set_index('date')
df['ema'] = df['total_sales'].ewm(alpha = 0.3, adjust = False).mean()
print(df['ema'])

# quantilys 
quantilys_90 = df['total_sales'].quantile(0.9)
df['is_quantiles']  = df['total_sales'] > quantilys_90

top_3 = df.groupby(
       ['product_id', 'date']
)['total_sales'].agg('mean').reset_index()[['product_id','total_sales']].nlargest(
    3, 'total_sales'
)
print(top_3)
