#  leetcode problem (1251. Average Selling Price)
                # leetcode problem (1251. Average Selling Price)
import pandas as pd


def average_selling_price(prices: pd.DataFrame, units_sold: pd.DataFrame) -> pd.DataFrame:
    # Merge the dataframes
    merged_df = pd.merge(prices, units_sold, on='product_id', how='left')
    
    # Filter rows where purchase_date is within start_date and end_date
    merged_df = merged_df[
        (merged_df['purchase_date'] >= merged_df['start_date']) &
        (merged_df['purchase_date'] <= merged_df['end_date'])
    ]
    
    # Calculate total price and units for each product_id
    merged_df['total_price'] = merged_df['units'] * merged_df['price']
    total_data = merged_df.groupby('product_id').agg(
        total_units=('units', 'sum'),
        total_price=('total_price', 'sum')
    ).reset_index()
    
    # Calculate average_price
    total_data['average_price'] = (total_data['total_price'] / total_data['total_units']).round(2)
    
    # Include products with no sales
    all_products = prices[['product_id']].drop_duplicates()
    result = pd.merge(all_products, total_data, on='product_id', how='left')
    result['average_price'] = result['average_price'].fillna(0)
    
    # Return final result
    return result[['product_id', 'average_price']]


# leetcode problem (1280. Students and Examinations )

import pandas as pd

def students_and_examinations(students: pd.DataFrame, subjects: pd.DataFrame, examinations: pd.DataFrame) -> pd.DataFrame:
    # Step 1: Create a cartesian join of all students and subjects
    cartesian_product = pd.merge(students[['student_id', 'student_name']], 
                                 subjects[['subject_name']], 
                                 how='cross')
    
    # Step 2: Count how many times each student attended each exam
    exam_count = examinations.groupby(['student_id', 'subject_name']).size().reset_index(name='attended_exams')

    # Step 3: Merge the cartesian join with the exam counts
    result = pd.merge(cartesian_product, exam_count, 
                      left_on=['student_id', 'subject_name'], 
                      right_on=['student_id', 'subject_name'], 
                      how='left').fillna({'attended_exams': 0})
    
    # Step 4: Clean up the final table, reorder columns, and sort
    result = result[['student_id', 'student_name', 'subject_name', 'attended_exams']]
    result = result.sort_values(by=['student_id', 'subject_name'], ascending=[True, True])
    
    return result

