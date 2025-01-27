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


'''

Problem 2: Advanced Groupby with Hierarchical Indexing and Complex Aggregation
You have a dataset that tracks users' interactions with a recommendation system across multiple sessions.

Dataset columns:

session_id: Unique identifier for each session
user_id: Unique identifier for each user
category: The category of items viewed (e.g., "sports", "technology")
view_time: Time spent on the recommendation page
clicked: Boolean indicating whether the user clicked an item during that session
timestamp: Exact timestamp of the session start
Task:

Group the data by user_id and category and calculate the following:
Total number of sessions
Total view time
Click-through rate (CTR): clicked / sessions
Average view time per session
Create a hierarchical index with user_id and category, and compute:
The user's category preference (i.e., which category they spent the most time on across sessions)
A rolling window of 3 sessions to compute the average view time and CTR.
Calculate the difference in click-through rates (CTR) before and after the user's preference for a particular category was established (i.e., when the total view time for that category is higher than for other categories).
Create a heatmap of the CTR for each user_id and category combination to identify any significant patterns.
'''


import pandas as pd

# Create a sample dataset
data = {
    "session_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "user_id": [101, 101, 102, 102, 103, 103, 104, 104, 105, 105],
    "category": ["sports", "technology", "sports", "sports", "technology", "sports", "sports", "technology", "sports", "technology"],
    "view_time": [12, 5, 8, 15, 10, 14, 7, 6, 11, 9],
    "clicked": [True, False, True, False, True, False, True, False, True, False],
    "timestamp": pd.to_datetime([
        "2025-01-01 10:00:00", "2025-01-01 10:30:00", "2025-01-01 11:00:00",
        "2025-01-01 11:30:00", "2025-01-01 12:00:00", "2025-01-01 12:30:00",
        "2025-01-01 13:00:00", "2025-01-01 13:30:00", "2025-01-01 14:00:00",
        "2025-01-01 14:30:00"
    ])
}

df = pd.DataFrame(data)

# 1ST PROBLEMS  
total_sessions = df.groupby(['user_id', 'category'])['session_id'].transform('count')
total_view_time = df.groupby(['user_id', 'category'])['view_time'].transform('sum')
click_through_rate = df.groupby(['user_id', 'category']).apply(
    lambda x : x['clicked'].sum() / x['session_id'].unique().sum()
)
df['average_view_time']  = df.groupby('session_id')['view_time'].transform('mean') 
