# ☕ Coffee Shop Sales Dashboard

An interactive sales analytics dashboard built with Streamlit and Plotly for visualizing coffee shop business metrics and trends.

🔗 **[Live Dashboard](https://simple-coffee-shop-sales-dashboard-iki.streamlit.app)**

## 📊 Dashboard Overview

This dashboard provides comprehensive insights into coffee shop sales performance through interactive visualizations and key performance indicators.

### Key Performance Indicators (KPIs)

**When viewing all months:**

- **Total Sales** - Overall revenue across all transactions
- **Total Orders** - Total number of unique transactions
- **Total Quantity Sold** - Sum of all items sold

**When filtering by specific month:**

- Shows month-over-month percentage growth for each metric
- Displays mini trend line charts showing daily patterns within the selected month
- Color-coded delta indicators (green for increase, red for decrease)

### Visualizations

#### 1. Sales Trend over the Period

A bar chart showing daily sales with an average sales benchmark line. Helps identify high and low performing days at a glance.

#### 2. Sales by Days | Hours (Heatmap)

Interactive heatmap displaying sales performance across:

- **Rows**: Hours of the day (0-23)
- **Columns**: Days of the week (Monday-Sunday)
- **Side bar**: Hourly totals showing peak business hours

Color intensity indicates sales volume, making it easy to spot peak times and optimize staffing.

#### 3. Sales by Product Category

Horizontal bar chart showing top 10 product categories ranked by total sales revenue.

#### 4. Sales by Products

Horizontal bar chart displaying top 10 individual products ranked by total sales revenue.

#### 5. Sales by Weekday/Weekend

Donut chart comparing revenue distribution between weekdays and weekend days, with total revenue displayed in the center.

#### 6. Sales by Store Location

Horizontal bar chart showing sales performance across different store locations.

## 🎯 Features

- **Month Filter**: Dropdown in sidebar to filter data by month (January-June) or view all months
- **Dynamic Updates**: All charts and KPIs update automatically based on selected month
- **Custom Color Scheme**: Coffee-themed brown color palette (#b5643b, #924421)
- **Responsive Layout**: Wide layout optimized for desktop viewing

## 📁 Project Structure

```
├── app.py              # Main Streamlit application
├── components.py       # Charts class with visualization logic
└── data/
    └── coffee.csv      # Sales transaction data
```

## 📋 Data Requirements

The dashboard expects a CSV file with the following columns:

| Column             | Description                      | Format Example |
| ------------------ | -------------------------------- | -------------- |
| `transaction_id`   | Unique transaction identifier    | Any unique ID  |
| `transaction_date` | Date of transaction              | dd/mm/yyyy     |
| `transaction_time` | Time of transaction              | HH:MM:SS       |
| `transaction_qty`  | Quantity of items in transaction | Integer        |
| `unit_price`       | Price per unit                   | Float/Decimal  |
| `product_category` | Product category name            | Text           |
| `product_type`     | Specific product name            | Text           |
| `store_location`   | Store location identifier        | Text           |

## 🔧 Technical Implementation

### Data Processing

The `Charts` class in `components.py` handles all data processing and visualization:

**Preprocessing:**

- Combines date and time into datetime object
- Extracts month, day name, and hour from datetime
- Calculates total price (quantity × unit price)

**Filtering:**

- Applies month filter when selected
- Returns full dataset when "All" is selected

### Chart Methods

| Method                      | Purpose                                    | Returns         |
| --------------------------- | ------------------------------------------ | --------------- |
| `kpi_cards_no_filter()`     | Calculate overall KPIs                     | Tuple of values |
| `kpi_cards_with_filter()`   | Calculate monthly KPIs with growth metrics | DataFrame       |
| `kpi_line_graph()`          | Generate mini trend charts for KPI cards   | Plotly figure   |
| `sales_trend_period()`      | Daily sales bar chart with average line    | Plotly figure   |
| `sales_heamap()`            | Day/hour heatmap with hourly totals        | Plotly figure   |
| `sales_product_bar_chart()` | Top 10 products horizontal bar chart       | Plotly figure   |
| `sales_weekly()`            | Weekday vs weekend donut chart             | Plotly figure   |
| `sales_location()`          | Store location horizontal bar chart        | Plotly figure   |

## 🎨 Design Choices

**Color Palette:**

- Primary: `#b5643b` (Warm brown)
- Secondary: `#924421` (Dark brown)
- Gradient scale: `#d98967` → `#6e240e`

**Layout:**

- Wide mode for maximum chart visibility
- Sidebar for filtering controls
- 3-column grid for KPIs
- Responsive chart sizing

## 💡 Business Insights

This dashboard helps answer key business questions:

- What are our peak sales hours and days?
- Which products drive the most revenue?
- How does performance vary by location?
- Are we growing month-over-month?
- Do we perform better on weekdays or weekends?

---

**Built with:** Python · Streamlit · Plotly · Pandas · NumPy
