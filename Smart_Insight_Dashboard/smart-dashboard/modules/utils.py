import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def format_currency(value):
    """Format number as currency string."""
    return f"${value:,.2f}"

def format_percentage(value):
    """Format number as percentage string."""
    return f"{value:.1f}%"

def get_date_range(df, date_col='order_date'):
    """Get min and max date from dataframe."""
    return df[date_col].min(), df[date_col].max()

def filter_data_by_date(df, start_date, end_date, date_col='order_date'):
    """Filter dataframe by date range."""
    mask = (df[date_col].dt.date >= start_date) & (df[date_col].dt.date <= end_date)
    return df.loc[mask]
