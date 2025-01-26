import pandas as p
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

df['date'] = pd.to_datetime(df['date'] ) 

df['daily_sales'] = df['price'] * df['quantity']
df.set_index(['category','product_id','user_id','date'],inplace = True)

final_df = pd.DateFrame()
for (category,product_id,user_id) , group in df.groupby(['category','product_id','user_id']):
    min_date = df[(df["category"] == category) & (df["product_id"] == product_id) & (df["user_id"] == user_id)]["date"].min()

max_date = df[(df["category"] == category) & (df["product_id"] == product_id) & (df["user_id"] == user_id)]["date"].max()

date_range = pd.date_range(start = min_date , end = max_date , freq = "D")

date_range_df = pd.DataFrame(date_range, columns = ["date"])
date_range_df.set_index("date",inplace = True)
date_range_df["category"] = category
date_range_df["product_id"] = product_id 
date_range_df["user_id"] = user_id 

merge_data = data_range_df.merge(group[['daily_sales']],left_index= True,right_index = True, how = "left")

merge_data["daily_sales"] = merge_data['daily_sales'].fillna(method = "ffill")

final_df = pd.concat([final_df,merge_data])
