import pandas as pd

# Step 1: Read the CSV files
products_df = pd.read_csv('products.csv')
sales_df = pd.read_csv('sales.csv')

# Step 2: Merge on 'sku' and fill missing sales with 0
df = pd.merge(products_df, sales_df, on='sku', how='left').fillna(0)

# Step 3: Apply pricing rules function
def apply_pricing_rules(row):
    current_price = row['current_price']
    cost_price = row['cost_price']
    stock = row['stock']
    quantity_sold = row['quantity_sold']
    new_price = current_price

    # Rule 1 – Low Stock, High Demand
    if stock < 20 and quantity_sold > 30:
        new_price = current_price * 1.15
    # Rule 2 – Dead Stock
    elif stock > 200 and quantity_sold == 0:
        new_price = current_price * 0.70
    # Rule 3 – Overstocked Inventory
    elif stock > 100 and quantity_sold < 20:
        new_price = current_price * 0.90

    # Rule 4 – Minimum Profit Constraint
    min_price = cost_price * 1.2
    if new_price < min_price:
        new_price = min_price

    # Final rounding
    return round(current_price, 2), round(new_price, 2)

# Step 4: Apply the rules to each row
df[['old_price', 'new_price']] = df.apply(apply_pricing_rules, axis=1, result_type='expand')

# Step 5: Add units to prices
df['old_price'] = df['old_price'].apply(lambda x: f"{x:.2f} INR")
df['new_price'] = df['new_price'].apply(lambda x: f"{x:.2f} INR")

# Step 6: Create output file
output_df = df[['sku', 'old_price', 'new_price']]
output_df.to_csv('updated_prices.csv', index=False)

print("✅ updated_prices.csv generated successfully!")
