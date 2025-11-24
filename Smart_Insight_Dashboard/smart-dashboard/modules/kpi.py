import pandas as pd
import numpy as np

class KPIEngine:
    def __init__(self, df):
        self.df = df
        
    def calculate_kpis(self):
        """Calculate core KPIs."""
        total_sales = self.df['sales'].sum()
        total_profit = self.df['profit'].sum()
        total_orders = self.df['order_id'].nunique()
        avg_order_value = total_sales / total_orders if total_orders > 0 else 0
        profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
        
        return {
            'total_sales': total_sales,
            'total_profit': total_profit,
            'total_orders': total_orders,
            'avg_order_value': avg_order_value,
            'profit_margin': profit_margin
        }
        
    def calculate_growth(self):
        """Calculate MoM and YoY growth."""
        # Monthly aggregation
        monthly = self.df.groupby(self.df['order_date'].dt.to_period('M'))['sales'].sum()
        
        if len(monthly) < 2:
            return {'mom_growth': 0, 'yoy_growth': 0}
            
        current_month = monthly.iloc[-1]
        last_month = monthly.iloc[-2]
        mom_growth = ((current_month - last_month) / last_month * 100) if last_month != 0 else 0
        
        # YoY (compare same month last year)
        if len(monthly) > 12:
            last_year_month = monthly.iloc[-13]
            yoy_growth = ((current_month - last_year_month) / last_year_month * 100) if last_year_month != 0 else 0
        else:
            yoy_growth = 0
            
        return {
            'mom_growth': mom_growth,
            'yoy_growth': yoy_growth
        }
        
    def get_region_performance(self):
        """Calculate normalized region performance score."""
        region_stats = self.df.groupby('region').agg({
            'sales': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        # Simple normalization: (Sales / Max Sales) * 0.5 + (Profit / Max Profit) * 0.5
        max_sales = region_stats['sales'].max()
        max_profit = region_stats['profit'].max()
        
        region_stats['performance_score'] = (
            (region_stats['sales'] / max_sales) * 50 + 
            (region_stats['profit'] / max_profit) * 50
        )
        
        return region_stats.sort_values('performance_score', ascending=False)
