# Smart Business Insights Dashboard 📊

A production-ready analytics dashboard powered by **Streamlit**, **Plotly**, and **OpenAI**.

## 🚀 Features

- **Interactive Dashboard**: Sales, Profit, and Customer analytics.
- **Forecasting**: SARIMA and Linear Regression models for future sales prediction.
- **AI Insights**: Automated business insights using OpenAI GPT-4o-mini.
- **Dynamic Filtering**: Date range and categorical filters.
- **Modern UI**: Glassmorphism design with custom CSS.

## 🛠 Tech Stack

- **Frontend**: Streamlit, Plotly, Custom CSS
- **Backend**: Python, Pandas, NumPy
- **ML/AI**: Statsmodels (SARIMA), Scikit-learn, OpenAI API
- **Data**: Synthetic Superstore Data (Auto-generated)

## 📂 Architecture

```
smart-dashboard/
├── app.py                 # Main Application Entry Point
├── Dockerfile             # Container Config
├── requirements.txt       # Dependencies
├── assets/
│   └── custom.css         # Styling
├── data/
│   └── sample_superstore.csv # Data (Generated on first run)
├── modules/
│   ├── loader.py          # Data Loading & Cleaning
│   ├── kpi.py             # KPI Calculations
│   ├── forecasting.py     # ML Models
│   ├── visualization.py   # Plotly Charts
│   ├── ai_engine.py       # OpenAI Integration
│   └── utils.py           # Utilities
└── tests/
    └── test_kpis.py       # Unit Tests
```

## 🏃 How to Run Locally

1.  **Clone/Navigate to directory**:
    ```bash
    cd smart-dashboard
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set OpenAI API Key (Optional)**:
    - Set `OPENAI_API_KEY` in your environment variables OR enter it in the UI.

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## 🐳 How to Deploy (Docker)

1.  **Build Image**:
    ```bash
    docker build -t smart-dashboard .
    ```

2.  **Run Container**:
    ```bash
    docker run -p 8501:8501 smart-dashboard
    ```

## 🧪 Running Tests

Run the unit tests to verify KPI calculations:

```bash
pytest tests/
```
