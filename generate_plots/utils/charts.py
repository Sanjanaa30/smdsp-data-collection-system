import matplotlib.pyplot as plt
import numpy as np


def bar_chart(chan_stats: dict, reddit_stats: dict, xlabel, ylabel, title):
    """
    Create a grouped bar chart comparing toxicity metrics between 4chan and Reddit.

    Args:
        chan_stats: Dictionary with toxicity metrics for 4chan
        reddit_stats: Dictionary with toxicity metrics for Reddit
    """
    # Extract metrics and values
    metrics = list(chan_stats.keys())
    chan_values = [chan_stats[metric] for metric in metrics]
    reddit_values = [reddit_stats[metric] for metric in metrics]

    # Set up the bar positions
    x = np.arange(len(metrics))
    width = 0.35  # Width of bars

    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 7))

    # Create bars
    bars1 = ax.bar(
        x - width / 2,
        chan_values,
        width,
        label="4chan",
        color="steelblue",
        edgecolor="black",
        linewidth=0.7,
    )
    bars2 = ax.bar(
        x + width / 2,
        reddit_values,
        width,
        label="Reddit",
        color="coral",
        edgecolor="black",
        linewidth=0.7,
    )

    # Customize the chart
    ax.set_xlabel(xlabel, fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=13, fontweight="bold")
    ax.set_title(title, fontsize=15, fontweight="bold", pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=45, ha="right")
    ax.legend(fontsize=11, loc="upper right")
    ax.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.7)

    # Add value labels on bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.3f}",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=0,
            )

    add_value_labels(bars1)
    add_value_labels(bars2)

    # Adjust layout and save
    plt.tight_layout()
    # Create output directory if it doesn't exist and save
    import os

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filename = title.replace(":", "").replace(" ", "_") + ".png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    print(f"\nChart saved as '{filepath}'")

    # Display the plot
    plt.show()
