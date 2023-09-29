import os
import csv
from faker import Faker

fake = Faker()

header = ['product_name', 'Category', 'Price',
          'customer_name', 'City', 'purchase_date']

# Define a function to get the next file name


def get_next_filename():
    index = 1
    while True:
        filename = f"ecommerce_data_{index}.csv"
        if not os.path.exists(filename):
            return filename
        index += 1


filename = get_next_filename()

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for _ in range(100):
        writer.writerow([
            fake.unique.first_name(),
            fake.random_element(elements=('Electronics', 'Clothes', 'Toys')),
            fake.random.randint(100, 1000),
            fake.name(),
            fake.city(),
            fake.date_this_decade()
        ])
