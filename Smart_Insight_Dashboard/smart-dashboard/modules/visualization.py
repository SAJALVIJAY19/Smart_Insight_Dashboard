import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Visualizer:
    def __init__(self, df):
        self.df = df
        
    def plot_sales_over_time(self, freq='M'):
        """Sales over time line chart."""
        data = self.df.groupby(pd.Grouper(key='order_date', freq=freq))['sales'].sum().reset_index()
        fig = px.line(data, x='order_date', y='sales', title='Sales Over Time',
                     template='plotly_white')
        fig.update_layout(hovermode="x unified")
        return fig
        
    def plot_profit_over_time(self, freq='M'):
        """Profit over time line chart."""
        data = self.df.groupby(pd.Grouper(key='order_date', freq=freq))['profit'].sum().reset_index()
        fig = px.line(data, x='order_date', y='profit', title='Profit Over Time',
                     line_shape='spline', color_discrete_sequence=['#2ca02c'])
        return fig
        
    def plot_category_sales(self):
        """Category-wise sales pie/bar chart."""
        data = self.df.groupby('category')['sales'].sum().reset_index()
        fig = px.pie(data, values='sales', names='category', title='Sales by Category',
                    hole=0.4)
        return fig
        
    def plot_region_map(self):
        """Region revenue bar chart (Map placeholder as we don't have lat/lon)."""
        data = self.df.groupby('region')['sales'].sum().reset_index()
        fig = px.bar(data, x='region', y='sales', color='sales', title='Revenue by Region',
                    color_continuous_scale='Viridis')
        return fig
        
    def plot_top_products(self, n=10):
        """Top N products by sales."""
        data = self.df.groupby('product_name')['sales'].sum().nlargest(n).reset_index()
        fig = px.bar(data, x='sales', y='product_name', orientation='h', 
                    title=f'Top {n} Products', color='sales')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        return fig
        
    def plot_discount_vs_sales(self):
        """Scatter plot of discount vs sales."""
        fig = px.scatter(self.df, x='discount', y='sales', color='category',
                        title='Discount vs Sales Correlation', opacity=0.6)
        return fig
        
    def plot_profitability_heatmap(self):
        """Heatmap of profit by Category and Region."""
        data = self.df.pivot_table(values='profit', index='category', columns='region', aggfunc='sum')
        fig = px.imshow(data, title='Profitability Heatmap (Category vs Region)',
                       color_continuous_scale='RdBu')
        return fig
        
    def plot_monthly_trends(self):
        """Monthly seasonality."""
        df_copy = self.df.copy()
        df_copy['month_name'] = df_copy['order_date'].dt.month_name()
        df_copy['month_num'] = df_copy['order_date'].dt.month
        data = df_copy.groupby(['month_num', 'month_name'])['sales'].mean().reset_index()
        data = data.sort_values('month_num')
        
        fig = px.bar(data, x='month_name', y='sales', title='Average Monthly Sales Trend')
        return fig

    def plot_forecast(self, history_df, forecast_df):
        """Plot historical data and forecast."""
        fig = go.Figure()
        
        # Historical
        fig.add_trace(go.Scatter(x=history_df.index, y=history_df['sales'], 
                                mode='lines', name='Historical Sales'))
        
        # Forecast
        if not forecast_df.empty:
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['predicted'],
                                    mode='lines', name='Forecast', line=dict(dash='dash')))
            
            # Confidence Interval
            fig.add_trace(go.Scatter(
                x=pd.concat([pd.Series(forecast_df.index), pd.Series(forecast_df.index[::-1])]),
                y=pd.concat([forecast_df['upper_ci'], forecast_df['lower_ci'][::-1]]),
                fill='toself',
                fillcolor='rgba(0,100,80,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=False,
                name='Confidence Interval'
            ))
            
        fig.update_layout(title='Sales Forecast with Confidence Intervals')
        return fig
