import pytest
import pandas as pd
import numpy as np
from modules.kpi import KPIEngine

@pytest.fixture
def sample_df():
    data = {
        'sales': [100, 200, 300, 400],
        'profit': [10, 20, 30, 40],
        'order_id': ['O1', 'O2', 'O3', 'O4'],
        'order_date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-02-01', '2023-02-02']),
        'region': ['North', 'North', 'South', 'South']
    }
    return pd.DataFrame(data)

def test_calculate_kpis(sample_df):
    engine = KPIEngine(sample_df)
    kpis = engine.calculate_kpis()
    
    assert kpis['total_sales'] == 1000
    assert kpis['total_profit'] == 100
    assert kpis['total_orders'] == 4
    assert kpis['avg_order_value'] == 250.0
    assert kpis['profit_margin'] == 10.0

def test_region_performance(sample_df):
    engine = KPIEngine(sample_df)
    perf = engine.get_region_performance()
    
    assert len(perf) == 2
    assert 'performance_score' in perf.columns
    # South has higher sales (700 vs 300), so should be ranked higher or equal depending on normalization
    assert perf.iloc[0]['region'] == 'South'
