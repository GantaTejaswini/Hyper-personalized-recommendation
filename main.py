import pandas as pd
import numpy as np
import sqlite3
import random

# Load datasets
customer_df = pd.read_csv("data/customer_data_collection.csv")
product_df = pd.read_csv("data/product_recommendation_data.csv")

# Connect to SQLite database
conn = sqlite3.connect("backend/memory.db")
cursor = conn.cursor()

# Create interactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    customer_id TEXT,
    product_id TEXT,
    reward INTEGER
)
""")
conn.commit()

# Store interaction in database
def store_interaction(customer_id, product_id, reward):
    cursor.execute(
        "INSERT INTO interactions (customer_id, product_id, reward) VALUES (?, ?, ?)",
        (customer_id, product_id, reward)
    )
    conn.commit()

# Bandit Algorithm Class
class MultiArmedBandit:
    def __init__(self, product_df):
        self.product_df = product_df
        self.product_stats = {product_id: [1, 1] for product_id in product_df['Product_ID']}

    def select_product(self):
        product_scores = {}
        for product_id, (success, total) in self.product_stats.items():
            score = np.random.beta(success, total - success + 1)
            product_scores[product_id] = score
        best_product = max(product_scores, key=product_scores.get)
        return best_product

    def update_rewards(self, customer_id, product_id, reward):
        success, total = self.product_stats.get(product_id, [1, 1])
        self.product_stats[product_id] = [success + reward, total + 1]
        store_interaction(customer_id, product_id, reward)

# Select a random customer for simulation
customer_row = customer_df.sample(1).iloc[0]
customer_id = customer_row['Customer_ID']

# Initialize bandit and recommend a product
bandit = MultiArmedBandit(product_df)
selected_product = bandit.select_product()
print(f"Recommended Product ID: {selected_product}")

# Simulate feedback (1 = purchased, 0 = ignored)
customer_feedback = random.choice([0, 1])

# Update rewards and memory
bandit.update_rewards(customer_id, selected_product, customer_feedback)

# Show interaction history
history = pd.read_sql_query("SELECT * FROM interactions", conn)
print("\nInteraction History:")
print(history.tail())

# Close connection
conn.close()
