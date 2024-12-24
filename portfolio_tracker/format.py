def plot_portfolio_distribution_3d(owned_assets_dict, current_stock_values):
    """
    Plots a 3D-like pie chart showing the distribution of the portfolio's value among the owned stocks.

    Parameters:
    - owned_assets_dict (dict): Dictionary where keys are stock names and values are total number of shares owned.
    - current_stock_values (dict): Dictionary where keys are stock names and values are current values in USD.
    """
    # Calculate the total value for each stock in the portfolio
    portfolio_values = {
        stock: owned_assets_dict[stock] * current_stock_values[stock]
        for stock in owned_assets_dict
    }

    # Extract the labels and values for the pie chart
    labels = list(portfolio_values.keys())
    sizes = list(portfolio_values.values())

    # Define colors for the chart
    colors = plt.cm.tab20.colors  # You can customize this as needed

    # Create an 'explode' list to create space between the slices
    explode = [0.05] * len(labels)  # Adjust the explode value to change the gap size

    # Number of layers to create the 3D effect
    layers = 5
    gap = 0.03  # Gap between layers

    fig, ax = plt.subplots(figsize=(8, 8))

    for i in range(layers):
        radius = 1 - i * gap
        if i == 0:
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                colors=colors,
                explode=explode,
                startangle=140,
                radius=radius,
                shadow=True,
                wedgeprops=dict(width=0.3, edgecolor="w"),
            )
        else:
            wedges, texts = ax.pie(
                sizes,
                labels=None,
                colors=colors,
                explode=explode,
                startangle=140,
                radius=radius,
                shadow=True,
                wedgeprops=dict(width=0.3, edgecolor="w"),
            )

    if "autotexts" in locals():
        # Adjust percentage labels to avoid overlap
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_bbox(dict(facecolor="white", edgecolor="none", alpha=0.6))

    # Use adjustText to avoid overlapping labels
    all_texts = texts + autotexts if "autotexts" in locals() else texts
    adjust_text(all_texts, arrowprops=dict(arrowstyle="-", color="gray", lw=0.5))

    ax.set_title("Stock Portfolio Distribution by Current Value")

    plt.show()


def plot_unrealized_gains(unrealized_gains):
    """
    Plots a bar chart of unrealized gains for each asset in the portfolio using Seaborn.

    Parameters:
    - unrealized_gains (dict): A dictionary where keys are stock names and values are unrealized gains in USD.
    """
    # Convert the dictionary to a DataFrame for easier plotting
    df = pd.DataFrame(
        list(unrealized_gains.items()), columns=["Stock", "Unrealized Gain"]
    )

    # Set the aesthetic style of the plots
    sns.set_style("whitegrid")

    # Create a seaborn barplot
    plt.figure(figsize=(12, 7))
    barplot = sns.barplot(x="Stock", y="Unrealized Gain", data=df, edgecolor="black")

    # Add title and labels
    plt.title("Unrealized Gains of Current Portfolio", fontsize=16)
    plt.xlabel("Stocks", fontsize=14)
    plt.ylabel("Unrealized Gains (USD)", fontsize=14)

    # Rotate x labels for better readability
    # barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=12)

    # Annotate each bar with the gain values
    for p in barplot.patches:
        barplot.annotate(
            f"{p.get_height():.2f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 10),
            textcoords="offset points",
            fontsize=12,
            fontweight="bold",
        )

    plt.tight_layout()
    plt.show()