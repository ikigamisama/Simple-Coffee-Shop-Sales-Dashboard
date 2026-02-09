import streamlit as st
from components import Charts

st.set_page_config(
    page_title="Coffee Shop Sales Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)


with st.sidebar:
    month_options = {
        "All": 0,
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6
    }

    # Streamlit selectbox
    month_name = st.selectbox(
        "Select Month",
        options=list(month_options.keys()),
        index=0
    )
value = month_options[month_name]
c = Charts(csv_file="data/coffee.csv", month=value)
st.header("☕ Coffee Shop Sales Dashboard")
st.caption("Track revenue, transactions, and peak hours at a glance")

if value == 0:
    total_sales, total_orders, total_quantity_sold = c.kpi_cards_no_filter()
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

    with kpi_col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")

    with kpi_col2:
        st.metric("Total Orders", f"${total_orders:,.2f}")

    with kpi_col3:
        st.metric("Total Quantity Sold", f"{total_quantity_sold:,}")

else:
    kpi_monthly_data, kpi_line_graph_data = c.kpi_cards_with_filter()
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric("Total Sales", f"${kpi_monthly_data['total_sales'].values[0]:,.2f}",
                  delta=f"{kpi_monthly_data['sales_percentage_growth'].values[0]:.2f}%",
                  delta_color="normal")

        st.plotly_chart(c.kpi_line_graph(kpi_line_graph_data,
                        y='total_price'), width='stretch')

    with kpi_col2:
        st.metric("Total Orders", f"{kpi_monthly_data['total_orders'].values[0]:,.0f}",
                  delta=f"{kpi_monthly_data['orders_percentage_growth'].values[0]:.2f}%",
                  delta_color="normal")

        st.plotly_chart(c.kpi_line_graph(kpi_line_graph_data,
                        y='total_orders'), width='stretch')

    with kpi_col3:
        st.metric("Total Quantity Sold", f"{kpi_monthly_data['total_quantity'].values[0]:,.0f}",
                  delta=f"{kpi_monthly_data['quantity_percentage_growth'].values[0]:.2f}%",
                  delta_color="normal")

        st.plotly_chart(c.kpi_line_graph(kpi_line_graph_data,
                        y='total_quantity'), width='stretch')


st.markdown("### Sales Trend over the Period")
st.plotly_chart(c.sales_trend_period(), width='stretch')

st.markdown("### Sales by Days | Hours")
st.plotly_chart(c.sales_heamap(), width='stretch')

sales_col1, sales_col2, sales_col3 = st.columns(3)

with sales_col1:
    st.markdown("#### Sales by Product category")
    st.plotly_chart(c.sales_product_bar_chart(
        'product_category'), width='stretch')


with sales_col2:
    st.markdown("#### Sales by Products")
    st.plotly_chart(c.sales_product_bar_chart(
        'product_type'), width='stretch')

with sales_col3:
    st.markdown("#### Sales by Weekday/Weekend")
    st.plotly_chart(c.sales_weekly(), width='stretch')

    st.markdown("#### Sales by Store Location")
    st.plotly_chart(c.sales_location(), width='stretch')
