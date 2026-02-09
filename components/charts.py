import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


class Charts:
    def __init__(self, csv_file, month=0):
        self.df = pd.read_csv(csv_file)
        self.original_df = self.df.copy()
        self.month = month
        self.data_preprocessing()

    def data_preprocessing(self):
        self.df['transaction_datetime'] = pd.to_datetime(
            self.df['transaction_date'] + " " + self.df['transaction_time'],
            format="%d/%m/%Y %H:%M:%S"
        )
        self.df['transaction_month'] = self.df['transaction_datetime'].dt.month
        self.df['transaction_day'] = self.df['transaction_datetime'].dt.day_name()
        self.df['transaction_hour'] = self.df['transaction_datetime'].dt.hour
        self.df['total_price'] = self.df['transaction_qty'] * \
            self.df['unit_price']

    def df_filtered_data(self):
        if self.month != 0:
            return self.df[self.df['transaction_month'] == self.month]
        else:
            return self.df.copy()

    def kpi_cards_no_filter(self):
        total_sales = self.df['total_price'].sum()
        total_orders = self.df['transaction_id'].nunique()
        total_quantity_sold = self.df['transaction_qty'].sum()

        return total_sales, total_orders, total_quantity_sold

    def kpi_cards_with_filter(self):
        kpi_monthly = self.df.groupby('transaction_month').agg(
            total_sales=('total_price', 'sum'),
            total_orders=('transaction_id', 'nunique'),
            total_quantity=('transaction_qty', 'sum')
        ).reset_index()

        kpi_monthly['sales_percentage_growth'] = kpi_monthly['total_sales'].pct_change(
        ) * 100
        kpi_monthly['sales_grown_from_prev'] = kpi_monthly['total_sales'].diff()
        kpi_monthly['sales_trend_direction'] = np.where(
            kpi_monthly['sales_percentage_growth'] > 0, 'Increasing',
            np.where(kpi_monthly['sales_percentage_growth']
                     < 0, 'Decreasing', 'No Change')
        )

        kpi_monthly['orders_percentage_growth'] = kpi_monthly['total_orders'].pct_change(
        ) * 100
        kpi_monthly['orders_grown_from_prev'] = kpi_monthly['total_orders'].diff()
        kpi_monthly['orders_trend_direction'] = np.where(
            kpi_monthly['orders_percentage_growth'] > 0, 'Increasing',
            np.where(kpi_monthly['orders_percentage_growth']
                     < 0, 'Decreasing', 'No Change')
        )
        kpi_monthly['quantity_percentage_growth'] = kpi_monthly['total_quantity'].pct_change(
        ) * 100
        kpi_monthly['quantity_grown_from_prev'] = kpi_monthly['total_quantity'].diff()
        kpi_monthly['quantity_trend_direction'] = np.where(
            kpi_monthly['quantity_percentage_growth'] > 0, 'Increasing',
            np.where(kpi_monthly['quantity_percentage_growth']
                     < 0, 'Decreasing', 'No Change')
        )
        kpi_monthly = kpi_monthly.fillna(0)
        kpi_monthly_data = kpi_monthly[kpi_monthly['transaction_month'] == self.month]

        kpi_line_graph_data = self.df[self.df['transaction_month'] == self.month]
        return kpi_monthly_data, kpi_line_graph_data

    def kpi_line_graph(self, kpi_line_graph, y):
        kpi_line_graph_df = kpi_line_graph.groupby('transaction_date').agg(
            total_price=('total_price', 'sum'),
            total_orders=('transaction_id', 'nunique'),
            total_quantity=('transaction_qty', 'sum')
        ).reset_index()

        fig = px.line(kpi_line_graph_df, x='transaction_date', y=y)
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=100,
        )

        # Remove grid lines
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        return fig

    def sales_trend_period(self):
        sales_trend_perday = self.df_filtered_data().groupby('transaction_date')[
            'total_price'].sum().rename('total_sales').reset_index()

        sales_trend_perday["transaction_date"] = pd.to_datetime(
            sales_trend_perday["transaction_date"],
            dayfirst=True
        )

        avg_sales = sales_trend_perday["total_sales"].mean()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=sales_trend_perday["transaction_date"],
            y=sales_trend_perday["total_sales"],
            marker_color="#b5643b",
            name="Daily Sales",
            showlegend=False
        ))

        # average line
        fig.add_trace(go.Scatter(
            x=sales_trend_perday["transaction_date"],
            y=[avg_sales] * len(sales_trend_perday),
            mode="lines",
            line=dict(color="white", dash="dash"),
            name=f"Average Sales ({avg_sales:,.2f})",
            showlegend=False
        ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Total Sales",
            height=600
        )

        return fig

    def sales_heamap(self):
        sales_by_days_hours = self.df_filtered_data().groupby(
            ['transaction_day', 'transaction_hour'])['total_price'].sum().rename('total_sales').reset_index()

        matrix_df = sales_by_days_hours.pivot(
            index="transaction_hour",
            columns="transaction_day",
            values="total_sales"
        ).sort_index(ascending=True)
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]
        matrix_df = matrix_df.fillna(0)
        matrix_df = matrix_df.reindex(columns=day_order)
        hourly_totals = matrix_df.sum(axis=1)

        brown_colorscale = [
            [0, '#d98967'],
            [0.2, '#ce8360'],
            [0.5, '#92482f'],
            [1, '#6e240e']
        ]

        fig = make_subplots(
            rows=1,
            cols=2,
            column_widths=[0.8, 0.2],
            shared_yaxes=True,
            horizontal_spacing=0.02
        )

        fig.add_trace(
            go.Heatmap(
                z=matrix_df.values,
                x=matrix_df.columns,
                y=matrix_df.index,
                colorscale=brown_colorscale,
                text=matrix_df.values,
                texttemplate="$%{text:,.0f}",
                showscale=False
            ),
            row=1,
            col=1
        )

        fig.add_trace(
            go.Bar(
                x=hourly_totals.values,
                y=hourly_totals.index,
                orientation="h",
                marker_color="#b5643b",
                text=hourly_totals.values,
                texttemplate="$%{text:,.0f}",
                textposition="outside",
                showlegend=False
            ),
            row=1,
            col=2
        )

        fig.update_layout(
            height=1000
        )

        fig.update_yaxes(autorange="reversed")

        return fig

    def sales_product_bar_chart(self, x):
        sales_product_category = self.df_filtered_data().groupby(
            x)['total_price'].sum().rename('total_sales').reset_index().sort_values(by='total_sales', ascending=True).head(10)

        categories = [
            {"name": row[x], "value": row["total_sales"]}
            for _, row in sales_product_category.iterrows()
        ]

        categories = sorted(
            categories,
            key=lambda x: x["value"],
            reverse=True
        )

        subplots = make_subplots(
            rows=len(categories),
            cols=1,
            subplot_titles=[x["name"] for x in categories],
            shared_xaxes=True,
            print_grid=False,
            vertical_spacing=(0.45 / len(categories)),
        )

        subplots.update_layout(
            showlegend=False,
        )

        for k, x in enumerate(categories):
            subplots.add_trace(
                go.Bar(
                    orientation="h",
                    y=[x["name"]],
                    x=[x["value"]],
                    text=["${:,.0f}".format(x["value"])],
                    hoverinfo="text",
                    textposition="auto",
                    marker=dict(color="#b5643b"),
                ),
                row=k + 1,
                col=1,
            )

        for ann in subplots.layout.annotations:
            ann.update(
                x=0,
                xanchor="left",
                align="left",
                font=dict(size=15),
            )

        for axis in subplots.layout:
            if axis.startswith("xaxis") or axis.startswith("yaxis"):
                subplots.layout[axis].visible = False

        height_calc = max(50 * len(categories), 700)

        subplots.update_layout(
            margin=dict(l=0, r=0, t=20, b=1),
            height=height_calc,
            width=height_calc,
        )

        return subplots

    def sales_weekly(self):
        sales_by_weekend = self.df_filtered_data().groupby('transaction_day')[
            'total_price'].sum().rename('total_sales').reset_index()
        sales_by_weekend['is_weekend'] = sales_by_weekend['transaction_day'].apply(
            lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')
        sales_by_weekday = sales_by_weekend.groupby(
            'is_weekend')['total_sales'].sum().reset_index()

        sales_by_weekend_total_sales = sales_by_weekend['total_sales'].sum().round(
            2).item()

        fig = go.Figure()
        label_colors = {"Weekend": "#924421", "Weekday": "#b5643b"}
        colors_list = [label_colors[label]
                       for label in sales_by_weekday["is_weekend"]]

        fig.add_trace(
            go.Pie(
                labels=sales_by_weekday["is_weekend"],
                values=sales_by_weekday["total_sales"],
                hole=0.7,
                marker=dict(colors=colors_list),
                showlegend=False,
                textposition="outside",
                texttemplate="<b>%{label}</b><br>$%{value:,.2f}<br>(%{percent})",
                textinfo="none",
            )
        )

        fig.update_layout(
            annotations=[dict(text=f"<b>${sales_by_weekend_total_sales:,.2f}</b><br>Revenue",
                              x=0.5,
                              y=0.5,
                              showarrow=False,
                              font_size=16)
                         ],
        )

        return fig

    def sales_location(self):
        sales_by_location = self.df_filtered_data().groupby('store_location')['total_price'].sum(
        ).rename('total_sales').reset_index().sort_values(by='total_sales', ascending=True)

        categories = [
            {"name": row["store_location"], "value": row["total_sales"]}
            for _, row in sales_by_location.iterrows()
        ]

        categories = sorted(
            categories,
            key=lambda x: x["value"],
            reverse=True
        )

        subplots = make_subplots(
            rows=len(categories),
            cols=1,
            subplot_titles=[x["name"] for x in categories],
            shared_xaxes=True,
            print_grid=False,
            vertical_spacing=(0.50 / len(categories)),
        )

        subplots.update_layout(
            showlegend=False,
        )

        for k, x in enumerate(categories):
            subplots.add_trace(
                go.Bar(
                    orientation="h",
                    y=[x["name"]],
                    x=[x["value"]],
                    text=["${:,.0f}".format(x["value"])],
                    hoverinfo="text",
                    textposition="auto",
                    marker=dict(color="#b5643b"),
                ),
                row=k + 1,
                col=1,
            )

        for ann in subplots.layout.annotations:
            ann.update(
                x=0,
                xanchor="left",
                align="left",
                font=dict(size=15),
            )

        for axis in subplots.layout:
            if axis.startswith("xaxis") or axis.startswith("yaxis"):
                subplots.layout[axis].visible = False

        height_calc = max(45 * len(categories), 300)

        subplots.update_layout(
            margin=dict(l=0, r=0, t=20, b=1),
            height=height_calc,
            width=height_calc,
        )

        return subplots
