import json
import pandas as pd

# Loads the data for the subcategories
with open('data/categories.json', 'r') as file:
    subcategories_list = json.load(file)


# Loads the data for the products
with open('data/products.json', 'r') as file:
    products_list = json.load(file)

# Products are in a list of lists, the list is flatten
flat_list = [item for sublist in products_list for item in sublist]

# Create data frames
products_df = pd.DataFrame(flat_list)
subcategory_df = pd.DataFrame(subcategories_list)

# Count the products per subcategory
subcategory_counts = products_df.groupby('subcategory_id').size().sort_values(ascending=False)

# Only keeps the subcategories with enough products
selected_subcategories = subcategory_counts.nlargest(100, keep='all')

# Get only data for needed subcategories
subcategories_final = subcategory_df[subcategory_df['id'].isin(selected_subcategories.index)]
products_final = products_df[products_df['subcategory_id'].isin(selected_subcategories.index)]

# Writes the information on json files
products_final.to_json('data/products_final.json', orient='records')
subcategories_final.to_json('data/subcategories_final.json', orient='records')
