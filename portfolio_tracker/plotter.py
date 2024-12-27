import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from plotly.graph_objects import Figure

from portfolio_tracker.config import config


def create_portfolio_distribution_plot(
    owned_assets_dict: dict,
    current_stock_values: dict,
) -> Figure:
    """Create a pie chart for portfolio distribution.

    :param owned_assets_dict:
    :param current_stock_values:
    :return: a go.Figure

    """
    portfolio_values = {
        stock: owned_assets_dict[stock] * current_stock_values[stock]
        for stock in owned_assets_dict
    }
    labels = list(portfolio_values.keys())
    sizes = list(portfolio_values.values())

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=sizes,
                textinfo="label+percent",
                hole=0.3,
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor=config.colors.bg_color,  # Background of the figure
        plot_bgcolor=config.colors.bg_color,  # Background of the plot area
        font=dict(color=config.colors.txt_color),  # Text color
    )
    return fig


def create_unrealized_gains_plot(
    unrealized_gains: dict,
) -> Figure:
    """Create a bar plot for unrealized gains.

    :param unrealized_gains:
    :return: a go.Figure

    """
    df = pd.DataFrame(
        list(unrealized_gains.items()), columns=["Ticker", "Unrealized Gain"]
    )
    fig = px.bar(df, x="Ticker", y="Unrealized Gain")
    fig.update_layout(
        paper_bgcolor=config.colors.bg_color,  # Background of figure
        plot_bgcolor=config.colors.bg_color,  # Background of plot area
        font=dict(color=config.colors.txt_color),  # Text color
    )
    fig.update_traces(
        marker_color=config.colors.blue_color,
        marker_line_color="black",
        marker_line_width=1,
    )
    return fig
