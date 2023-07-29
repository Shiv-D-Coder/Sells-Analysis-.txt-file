import re
import os

# Step 1: Get the list of files in the 'rfiles' directory
files = os.listdir('rfiles')
sorted_files = sorted(files)

# Step 2: Initialize variables for counting and storing data
total_lines = 0
valid_reviews_count = 0
product_ratings = {}

# Step 3: Process each file in the 'rfiles' directory
for filename in sorted_files:
    file_path = os.path.join('rfiles', filename)
    if os.path.isfile(file_path):
        # Open the file and process each line
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                total_lines += 1
                attributes = re.findall(r'<.*?>|\S+', line.strip())
                num_attributes = len(attributes)

                # Check if the line has 5 attributes, if so, it's a valid review
                if num_attributes == 5:
                    valid_reviews_count += 1
                    print(f"Line {line_num}: Valid - Number of attributes = {num_attributes}")
                    print(f"Customer ID: {attributes[0]}")
                    print(f"Product ID: {attributes[1]}")
                    print(f"Date: {attributes[2]}")
                    print(f"Rating: {attributes[3]}")
                    print(f"Review Text: {attributes[4][1:-1]}")

                    # Store the product ratings in a dictionary
                    if attributes[1] in product_ratings:
                        product_ratings[attributes[1]].append(float(attributes[3]))
                    else:
                        product_ratings[attributes[1]] = [float(attributes[3])]
                else:
                    print(f"Line {line_num}: Invalid - Expected 5 attributes, Found {num_attributes}")

# Step 4: Calculate average ratings for each product
average_ratings = {}
for product_id, ratings_list in product_ratings.items():
    # Remove any non-numeric characters from the ratings and calculate the average
    numeric_ratings = [rating for rating in ratings_list if isinstance(rating, (int, float))]
    average = sum(numeric_ratings) / len(numeric_ratings) if numeric_ratings else 0
    average_ratings[product_id] = average

# Step 5: Get the top 3 products based on average ratings
top_3_products = sorted(average_ratings.items(), key=lambda x: x[1], reverse=True)[:3]

# Step 6: Write the summary to a text file
with open('summary.txt', 'w') as file:
    file.write(f"Total reviews processed: {total_lines}\n")
    file.write(f"Total invalid reviews count: {total_lines - valid_reviews_count}\n")
    file.write(f"Total valid reviews count: {valid_reviews_count}\n")
    file.write("Top 3 products:\n")
    for product_id, avg_rating in top_3_products:
        file.write(f"Product ID: {product_id}, Average Rating: {avg_rating}\n")