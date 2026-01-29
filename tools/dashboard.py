import streamlit as st
import utils.db as db
import pandas as pd

def render():
    st.markdown("""
    <style>
        .metric-card {
            background: #FFFFFF;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            transition: border-color 0.2s ease;
        }
        .metric-card:hover {
            border-color: #0071E3;
        }
        .metric-title {
            color: #6B7280;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            color: #111827;
            font-size: 2.25rem;
            font-weight: 700;
            letter-spacing: -0.04em;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Trikon Performance Dashboard")
    
    data, total_count = db.get_stats()
    
    # Summary Metrics with Custom HTML
    col1, col2, col3 = st.columns(3)
    
    monthly_stats = db.get_monthly_stats()
    current_month = pd.Timestamp.now().strftime('%Y-%m')
    this_month_count = monthly_stats.get(current_month, 0)
    bc_count = len([x for x in data if x['tool'] == 'Business Card'])

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Generations</div>
            <div class="metric-value">{total_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">This Month</div>
            <div class="metric-value">{this_month_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Business Cards</div>
            <div class="metric-value">{bc_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # History Table
    if data:
        st.subheader("Generation History")
        df = pd.DataFrame(data)
        df = df[['created_at', 'tool', 'name', 'metadata']]
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Growth Trends")
        if monthly_stats:
            chart_data = pd.DataFrame(list(monthly_stats.items()), columns=['Month', 'Count']).sort_values('Month')
            # Custom line chart color
            st.line_chart(chart_data.set_index('Month'), color="#6366F1")
    else:
        st.info("No data available yet. Start generating cards to see stats!")
