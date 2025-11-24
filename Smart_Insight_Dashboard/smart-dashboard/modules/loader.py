import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from .utils import logger

class DataLoader:
    def __init__(self, data_path='data/sample_superstore.csv'):
        self.data_path = data_path
        
    def generate_synthetic_data(self):
        """Generate synthetic Superstore data if file doesn't exist."""
        logger.info("Generating synthetic data...")
        np.random.seed(42)
        
        # Date range
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2024, 12, 31)
        days = (end_date - start_date).days
        
        n_rows = 5000
        
        # Generate data
        dates = [start_date + timedelta(days=np.random.randint(0, days)) for _ in range(n_rows)]
        
        regions = ['North', 'South', 'East', 'West']
        categories = ['Furniture', 'Office Supplies', 'Technology']
        sub_categories = {
            'Furniture': ['Bookcases', 'Chairs', 'Tables', 'Furnishings'],
            'Office Supplies': ['Labels', 'Storage', 'Art', 'Binders', 'Appliances', 'Paper'],
            'Technology': ['Phones', 'Accessories', 'Copiers', 'Machines']
        }
        
        data = []
        for date in dates:
            cat = np.random.choice(categories)
            sub_cat = np.random.choice(sub_categories[cat])
            region = np.random.choice(regions)
            sales = np.random.uniform(10, 5000)
            quantity = np.random.randint(1, 15)
            discount = np.random.choice([0, 0.1, 0.2, 0.3, 0.5], p=[0.5, 0.2, 0.15, 0.1, 0.05])
            profit = sales * np.random.uniform(-0.2, 0.4) # Profit margin between -20% and 40%
            
            data.append({
                'order_id': f'ORD-{np.random.randint(10000, 99999)}',
                'order_date': date,
                'ship_date': date + timedelta(days=np.random.randint(2, 7)),
                'ship_mode': np.random.choice(['Standard Class', 'Second Class', 'First Class', 'Same Day']),
                'customer_id': f'CUST-{np.random.randint(1000, 9999)}',
                'customer_name': f'Customer {np.random.randint(1, 1000)}',
                'segment': np.random.choice(['Consumer', 'Corporate', 'Home Office']),
                'region': region,
                'state': 'Sample State', # Simplified
                'city': 'Sample City',   # Simplified
                'product_id': f'PROD-{cat[:3]}-{np.random.randint(1000, 9999)}',
                'category': cat,
                'sub_category': sub_cat,
                'product_name': f'{sub_cat} Product {np.random.randint(1, 100)}',
                'sales': round(sales, 2),
                'quantity': quantity,
                'discount': discount,
                'profit': round(profit, 2)
            })
            
        df = pd.DataFrame(data)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        df.to_csv(self.data_path, index=False)
        logger.info(f"Synthetic data saved to {self.data_path}")
        return df

    def load_data(self):
        """Load and preprocess data."""
        if not os.path.exists(self.data_path):
            df = self.generate_synthetic_data()
        else:
            df = pd.read_csv(self.data_path)
            
        # Preprocessing
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['ship_date'] = pd.to_datetime(df['ship_date'])
        
        # Handle missing values (simple imputation)
        df['sales'] = df['sales'].fillna(df['sales'].mean())
        df['profit'] = df['profit'].fillna(0)
        
        # Feature Engineering
        df['year'] = df['order_date'].dt.year
        df['month'] = df['order_date'].dt.month
        df['month_year'] = df['order_date'].dt.to_period('M')
        
        return df

    def get_monthly_aggregated(self, df):
        """Get monthly aggregated data."""
        monthly = df.groupby('month_year').agg({
            'sales': 'sum',
            'profit': 'sum',
            'quantity': 'sum',
            'order_id': 'nunique'
        }).reset_index()
        monthly['month_year'] = monthly['month_year'].dt.to_timestamp()
        return monthly
