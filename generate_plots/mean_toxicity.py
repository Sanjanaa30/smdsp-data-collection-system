import os
from utils.plsql import PLSQL
from constants.constants import ATTRIBUTE_OF_TOXICITY
from constants.plsql_constants import GET_CHAN_TOXICITY_QUERY, GET_REDDIT_TOXICITY_QUERY
import pandas as pd
import numpy as np
from utils.charts import bar_chart
from utils.logger import Logger

logger = Logger("mean_toxicity").get_logger()


def gather_data(database_url, query, params=None):
    try:
        logger.info(f"Gathering data from database with query limit: {params}")
        plsql = PLSQL(database_url=database_url)
        result = plsql.get_data_from(query, params)
        logger.info(f"Successfully retrieved {len(result)} records from database")
        return result
    except Exception as e:
        logger.error(f"Got an exception in gathering data: {e}")
        raise
    finally:
        plsql.close_connection()
        logger.debug("Database connection closed")


def get_stats(data: list):
    logger.info("Calculating statistics from data")
    header = ["Board Name", "Title or Comment", "post_no"] + ATTRIBUTE_OF_TOXICITY
    dataframe = pd.DataFrame(np.array(data), columns=header)
    logger.debug(f"DataFrame created with shape: {dataframe.shape}")
    logger.debug(f"DataFrame dtypes: {dataframe.dtypes}")

    result = {}
    for col in ATTRIBUTE_OF_TOXICITY:
        dataframe[col] = pd.to_numeric(dataframe[col])
        result[col] = dataframe[col].mean()
        logger.debug(f"Mean {col}: {result[col]:.4f}")

    logger.info("Statistics calculation completed")
    return result


def main(database_url, query):
    logger.info("Starting data collection and analysis")
    result = gather_data(database_url, query, 100)
    stats = get_stats(result)
    logger.info("Data collection and analysis completed")
    return stats


CHAN_DATABASE_URL = os.environ.get("CHAN_DATABASE_URL")
REDDIT_DATABASE_URL = os.environ.get("REDDIT_DATABASE_URL")

logger.info("=" * 60)
logger.info("Starting toxicity analysis for 4chan and Reddit")
logger.info("=" * 60)

logger.info("Processing 4chan data...")
chan_stats = main(CHAN_DATABASE_URL, GET_CHAN_TOXICITY_QUERY)
logger.info(f"4chan statistics: {chan_stats}")

logger.info("Processing Reddit data...")
reddit_stats = main(REDDIT_DATABASE_URL, GET_REDDIT_TOXICITY_QUERY)
logger.info(f"Reddit statistics: {reddit_stats}")

logger.info("Generating comparison bar chart...")
bar_chart(
    chan_stats,
    reddit_stats,
    "Toxicity Metrics",
    "Mean Score",
    "Mean Toxicity Scores Comparison: 4chan vs Reddit",
)
logger.info("Analysis complete!")
logger.info("=" * 60)
