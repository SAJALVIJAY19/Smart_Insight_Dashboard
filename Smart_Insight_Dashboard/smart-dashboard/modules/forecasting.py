import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.linear_model import LinearRegression
from .utils import logger

class ForecastEngine:
    def __init__(self, df):
        self.df = df
        
    def prepare_data(self, metric='sales', freq='M'):
        """Prepare time series data."""
        ts_data = self.df.groupby(pd.Grouper(key='order_date', freq=freq))[metric].sum().reset_index()
        ts_data = ts_data.set_index('order_date')
        return ts_data
        
    def sarima_forecast(self, periods=12):
        """Generate SARIMA forecast."""
        try:
            data = self.prepare_data()
            
            # Simple SARIMA configuration (auto-arima would be better but keeping it simple/fast)
            model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
            results = model.fit(disp=False)
            
            forecast = results.get_forecast(steps=periods)
            forecast_df = forecast.conf_int()
            forecast_df['predicted'] = forecast.predicted_mean
            forecast_df.columns = ['lower_ci', 'upper_ci', 'predicted']
            
            return forecast_df
        except Exception as e:
            logger.error(f"SARIMA forecast failed: {e}")
            return pd.DataFrame()

    def linear_trend(self, periods=12):
        """Generate Linear Regression trend."""
        try:
            data = self.prepare_data()
            data = data.reset_index()
            data['date_ordinal'] = data['order_date'].map(pd.Timestamp.toordinal)
            
            X = data[['date_ordinal']]
            y = data['sales']
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Future dates
            last_date = data['order_date'].max()
            future_dates = [last_date + pd.DateOffset(months=x) for x in range(1, periods + 1)]
            future_ordinals = [[d.toordinal()] for d in future_dates]
            
            predictions = model.predict(future_ordinals)
            
            return pd.DataFrame({
                'order_date': future_dates,
                'trend': predictions
            }).set_index('order_date')
        except Exception as e:
            logger.error(f"Linear trend failed: {e}")
            return pd.DataFrame()
