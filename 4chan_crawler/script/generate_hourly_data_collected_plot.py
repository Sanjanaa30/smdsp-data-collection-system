import matplotlib.pyplot as plt
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path to import from 4chan_crawler
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from constants.plsql_constants import SELECT_COUNT_BOARD_QUERY, SELECT_COUNT_HOUR_QUERY
from utils.plsql import PLSQL
from utils.logger import Logger

logger = Logger("Script Graphs").get_logger()

# Create output directory for graphs
OUTPUT_DIR = Path(__file__).resolve().parent / "graphs"
OUTPUT_DIR.mkdir(exist_ok=True)


def fetch_data(query):
    """Helper function to execute query and return data"""
    try:
        plsql = PLSQL()
        data = plsql.execute_query(query)
        plsql.close_connection()
        logger.info(f"Query executed successfully. Fetched {len(data)} rows.")
        return data
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return []


def plot_post_data(df, title, filename):
    """Helper function to plot post data by hour and save to file"""
    plt.figure(figsize=(12, 6))

    # Extract hour from datetime for x-axis
    df["hour_only"] = df["hour"].dt.hour

    # Plot for each board_name separately
    for board in df["board_name"].unique():
        board_data = df[df["board_name"] == board]
        plt.plot(
            board_data["hour_only"],
            board_data["post_count"],
            marker="o",
            label=board,
            linewidth=2,
        )

    # Customize the graph
    plt.xlabel("Hour of Day (0-23)")
    plt.ylabel("Post Count")
    plt.title(title)
    plt.legend(title="Board Names")
    plt.xticks(range(0, 24))  # Show all hours 0-23
    plt.grid(True, alpha=0.3)

    # Save the plot to file
    plt.tight_layout()
    output_path = OUTPUT_DIR / filename
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    logger.info(f"Graph saved to: {output_path}")
    plt.close()  # Close the figure to free memory


def process_data_for_plot(query, columns, title, filename):
    """Fetches data, processes it, and saves the graph"""
    data = fetch_data(query)
    logger.debug(f"fetched data {data}")

    if data:
        # Convert data to DataFrame for easy plotting
        df = pd.DataFrame(data, columns=columns)

        logger.debug(f"DataFrame shape: {df.shape}")
        logger.debug(f"DataFrame columns: {df.columns.tolist()}")
        logger.debug(f"DataFrame head:\n{df.head()}")

        # Plot the data and save to file
        plot_post_data(df, title, filename)
    else:
        logger.warning(f"No data available for query: {query}")


def main():
    """Main function to execute queries and save graphs"""
    # Fetch and plot board data (has 3 columns: board_name, hour, post_count)
    logger.info("Fetching board data...")
    process_data_for_plot(
        SELECT_COUNT_BOARD_QUERY,
        ["board_name", "hour", "post_count"],
        "Posts Collected per Board",
        "posts_per_board.png",
    )

    # Fetch and plot hourly data (has 2 columns: hour, post_count)
    logger.info("Fetching hourly data...")
    hourly_data = fetch_data(SELECT_COUNT_HOUR_QUERY)

    if hourly_data:
        df = pd.DataFrame(hourly_data, columns=["hour", "post_count"])
        df["hour_only"] = df["hour"].dt.hour

        plt.figure(figsize=(12, 6))
        plt.plot(
            df["hour_only"], df["post_count"], marker="o", linewidth=2, color="blue"
        )
        plt.xlabel("Hour of Day (0-23)")
        plt.ylabel("Total Post Count")
        plt.title("Total Posts Collected per Hour (All Boards)")
        plt.xticks(range(0, 24))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save the plot to file
        output_path = OUTPUT_DIR / "total_posts_per_hour.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        logger.info(f"Graph saved to: {output_path}")
        plt.close()
    else:
        logger.warning("No hourly data available")

    logger.info(f"All graphs saved successfully in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
