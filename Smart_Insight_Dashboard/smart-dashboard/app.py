import os
import streamlit as st
import pandas as pd
import plotly.express as px
from modules.loader import DataLoader
from modules.kpi import KPIEngine
from modules.visualization import Visualizer
from modules.forecasting import ForecastEngine
from modules.ai_engine import AIEngine
from modules.utils import format_currency, format_percentage

# Page Config
st.set_page_config(
    page_title="Smart Business Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Load CSS (correct path) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "assets", "custom.css")

try:
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning(f"Could not find CSS file at: {css_path}")
# ---------------------------------------------

# Initialize Modules
@st.cache_data
def load_data():
    loader = DataLoader()
    return loader.load_data()

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

kpi_engine = KPIEngine(df)
visualizer = Visualizer(df)
forecast_engine = ForecastEngine(df)
ai_engine = AIEngine()

# Sidebar
st.sidebar.title("📊 Smart Dashboard")
st.sidebar.markdown("---")

# Date Filter
min_date = df['order_date'].min().date()
max_date = df['order_date'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

# Filter Data
mask = (df['order_date'].dt.date >= start_date) & (df['order_date'].dt.date <= end_date)
filtered_df = df.loc[mask]

# Re-initialize engines with filtered data
kpi_engine_filtered = KPIEngine(filtered_df)
visualizer_filtered = Visualizer(filtered_df)

# Navigation
page = st.sidebar.radio("Navigate", ["Overview", "Sales Analytics", "Customers", "Forecasting", "AI Insights"])

st.sidebar.markdown("---")
st.sidebar.info("Built with Streamlit & OpenAI")

# --- OVERVIEW PAGE ---
if page == "Overview":
    st.title("🚀 Business Overview")
    
    # KPIs
    kpis = kpi_engine_filtered.calculate_kpis()
    growth = kpi_engine_filtered.calculate_growth()
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Sales", format_currency(kpis['total_sales']), f"{growth['mom_growth']:.1f}% MoM")
    col2.metric("Total Profit", format_currency(kpis['total_profit']), f"{growth['yoy_growth']:.1f}% YoY")
    col3.metric("Total Orders", kpis['total_orders'])
    col4.metric("Avg Order Value", format_currency(kpis['avg_order_value']))
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(visualizer_filtered.plot_sales_over_time(), use_container_width=True)
    with col2:
        st.plotly_chart(visualizer_filtered.plot_category_sales(), use_container_width=True)
        
    # Charts Row 2
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(visualizer_filtered.plot_region_map(), use_container_width=True)
    with col2:
        st.plotly_chart(visualizer_filtered.plot_top_products(), use_container_width=True)

# --- SALES ANALYTICS PAGE ---
elif page == "Sales Analytics":
    st.title("📈 Sales Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(visualizer_filtered.plot_profit_over_time(), use_container_width=True)
    with col2:
        st.plotly_chart(visualizer_filtered.plot_monthly_trends(), use_container_width=True)
        
    st.plotly_chart(visualizer_filtered.plot_profitability_heatmap(), use_container_width=True)
    
    with st.expander("Raw Data View"):
        st.dataframe(filtered_df)

# --- CUSTOMERS PAGE ---
elif page == "Customers":
    st.title("👥 Customer Insights")
    
    st.plotly_chart(visualizer_filtered.plot_discount_vs_sales(), use_container_width=True)
    
    # Simple Customer Segmentation (RFM-like)
    customer_stats = filtered_df.groupby('customer_name').agg({
        'sales': 'sum',
        'order_id': 'nunique',
        'order_date': 'max'
    }).reset_index()
    customer_stats.columns = ['Customer', 'Total Spend', 'Frequency', 'Last Order']
    
    st.subheader("Top Customers")
    st.dataframe(customer_stats.sort_values('Total Spend', ascending=False).head(10))

# --- FORECASTING PAGE ---
elif page == "Forecasting":
    st.title("🔮 AI Forecasting")
    
    forecast_periods = st.slider("Forecast Months", 1, 24, 12)
    
    tab1, tab2 = st.tabs(["SARIMA Model", "Linear Trend"])
    
    with tab1:
        st.subheader("SARIMA Sales Forecast")
        with st.spinner("Generating Forecast..."):
            forecast_df = forecast_engine.sarima_forecast(periods=forecast_periods)
            history_df = forecast_engine.prepare_data()
            
            if not forecast_df.empty:
                st.plotly_chart(visualizer.plot_forecast(history_df, forecast_df), use_container_width=True)
                
                # AI Interpretation
                if st.button("Interpret Forecast with AI"):
                    context = f"Forecast for next {forecast_periods} months: {forecast_df['predicted'].mean():.2f} average sales."
                    insight = ai_engine.generate_insight(context, 'forecast_interpretation')
                    st.info(insight)
            else:
                st.error("Forecast generation failed. Check data sufficiency.")
                
    with tab2:
        st.subheader("Linear Trend Analysis")
        trend_df = forecast_engine.linear_trend(periods=forecast_periods)
        if not trend_df.empty:
            fig = px.line(trend_df, title="Linear Trend Projection")
            st.plotly_chart(fig, use_container_width=True)

# --- AI INSIGHTS PAGE ---
elif page == "AI Insights":
    st.title("🤖 AI Insight Engine")
    
    api_key = st.text_input("Enter OpenAI API Key (if not in env)", type="password")
    if api_key:
        ai_engine = AIEngine(api_key)
    
    insight_type = st.selectbox("Select Insight Type", [
        "Executive Summary",
        "Trend Analysis",
        "Regional Performance",
        "Anomaly Detection",
        "Discount Strategy"
    ])
    
    if st.button("Generate Insight"):
        with st.spinner("Analyzing data..."):
            # Prepare context based on selection
            if insight_type == "Executive Summary":
                context = kpi_engine_filtered.calculate_kpis()
                prompt_type = 'executive_summary'
            elif insight_type == "Trend Analysis":
                context = filtered_df.groupby('month_year')['sales'].sum().to_dict()
                prompt_type = 'trend_summary'
            elif insight_type == "Regional Performance":
                context = kpi_engine_filtered.get_region_performance().to_dict()
                prompt_type = 'region_performance'
            elif insight_type == "Discount Strategy":
                context = filtered_df[['discount', 'sales', 'profit']].corr().to_dict()
                prompt_type = 'discount_causality'
            else:
                context = filtered_df.describe().to_string()
                prompt_type = 'anomaly_detection'
                
            insight = ai_engine.generate_insight(str(context), prompt_type)
            
            st.markdown("### 💡 AI Analysis")
            st.write(insight)
