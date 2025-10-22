import time
from reddit_client import RedditClient
from constants.api_constants import SUBREDDIT_URL
from constants.constants import REDDIT_CRAWLER, FAKTORY_CONSUMER_ROLE, POST_FIELDS
from modal.post import Post
from utils.logger import Logger
from utils.plsql import PLSQL
from constants.plsql_constants import BULK_INSERT_COMMUNITIES, SELECT_unique_name_QUERY
import json
from utils.faktory import init_faktory_client

logger = Logger(REDDIT_CRAWLER).get_logger()
reddit_client = RedditClient()


def fetch_posts(after=None) -> tuple[list[Post], str | None]:
    """
    Fetches subreddit data from Reddit API starting from `after` cursor.
    Returns a list of Communities objects and next page cursor.
    """
    params = {"limit": 100}
    if after:
        params["after"] = after

    # Test data

    response = "{\"kind\":\"Listing\",\"data\":{\"after\":\"t3_1ocgcrr\",\"dist\":25,\"modhash\":\"\",\"geo_filter\":null,\"children\":[{\"kind\":\"t3\",\"data\":{\"approved_at_utc\":null,\"subreddit\":\"technology\",\"selftext\":\"\",\"author_fullname\":\"t2_anc6u2m\",\"saved\":false,\"mod_reason_title\":null,\"gilded\":0,\"clicked\":false,\"title\":\"AWScrashcauses$2,000SmartBedstooverheatandgetstuckupright\",\"link_flair_richtext\":[],\"subreddit_name_prefixed\":\"r/technology\",\"hidden\":false,\"pwls\":6,\"link_flair_css_class\":\"general\",\"downs\":0,\"thumbnail_height\":78,\"top_awarded_type\":null,\"hide_score\":true,\"name\":\"t3_1ocgytv\",\"quarantine\":false,\"link_flair_text_color\":\"dark\",\"upvote_ratio\":0.98,\"author_flair_background_color\":null,\"ups\":4002,\"total_awards_received\":0,\"media_embed\":{},\"thumbnail_width\":140,\"author_flair_template_id\":null,\"is_original_content\":false,\"user_reports\":[],\"secure_media\":null,\"is_reddit_media_domain\":false,\"is_meta\":false,\"category\":null,\"secure_media_embed\":{},\"link_flair_text\":\"Hardware\",\"can_mod_post\":false,\"score\":4002,\"approved_by\":null,\"is_created_from_ads_ui\":false,\"author_premium\":false,\"thumbnail\":\"https://external-preview.redd.it/q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts.jpeg?width=140&height=78&auto=webp&s=831153b9ed01a229135495e7625bf3d2f81c5f7f\",\"edited\":false,\"author_flair_css_class\":null,\"author_flair_richtext\":[],\"gildings\":{},\"post_hint\":\"link\",\"content_categories\":null,\"is_self\":false,\"subreddit_type\":\"public\",\"created\":1761062652,\"link_flair_type\":\"text\",\"wls\":6,\"removed_by_category\":null,\"banned_by\":null,\"author_flair_type\":\"text\",\"domain\":\"dexerto.com\",\"allow_live_comments\":false,\"selftext_html\":null,\"likes\":null,\"suggested_sort\":null,\"banned_at_utc\":null,\"url_overridden_by_dest\":\"https://www.dexerto.com/entertainment/aws-crash-causes-2000-smart-beds-to-overheat-and-get-stuck-upright-3272251/\",\"view_count\":null,\"archived\":false,\"no_follow\":false,\"is_crosspostable\":false,\"pinned\":false,\"over_18\":false,\"preview\":{\"images\":[{\"source\":{\"url\":\"https://external-preview.redd.it/q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts.jpeg?auto=webp&s=e13d7501946b7851da64e636ab399cd0699d82ac\",\"width\":1600,\"height\":900},\"resolutions\":[{\"url\":\"https://external-preview.redd.it/q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts.jpeg?width=108&crop=smart&auto=webp&s=7f75cbe92b123ce00c73d02c8195464f732f07b6\",\"width\":108,\"height\":60},{\"url\":\"https://external-preview.redd.it/q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts.jpeg?width=216&crop=smart&auto=webp&s=95ac33371450dad0a4d89dbb8760343f1c583157\",\"width\":216,\"height\":121},{\"url\":\"https://external-preview.redd.it/q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts.jpeg?width=320&crop=smart&auto=webp&s=eadbe1bb3c48faa96cde3c51db7f580f25a67735\",\"width\":320,\"height\":180},{\"url\":\"https://external-preview.redd.it/q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts.jpeg?width=640&crop=smart&auto=webp&s=aea51a28c54dfb5d58e1a7a08e296e1daf711e63\",\"width\":640,\"height\":360},{\"url\":\"https://external-preview.redd.it/q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts.jpeg?width=960&crop=smart&auto=webp&s=b966c764f152305e9b57f691f7f0043b6c3d5ad1\",\"width\":960,\"height\":540},{\"url\":\"https://external-preview.redd.it/q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts.jpeg?width=1080&crop=smart&auto=webp&s=7e4f8f94bfd6deb271be11c061b8a9dc29617037\",\"width\":1080,\"height\":607}],\"variants\":{},\"id\":\"q6wYlURe1pLNsLYJz97VddCHgrsoDKItL32rbG0y7ts\"}],\"enabled\":false},\"all_awardings\":[],\"awarders\":[],\"media_only\":false,\"link_flair_template_id\":\"51f3078c-a816-11e9-914b-0e1d353d3716\",\"can_gild\":false,\"spoiler\":false,\"locked\":false,\"author_flair_text\":null,\"treatment_tags\":[],\"visited\":false,\"removed_by\":null,\"mod_note\":null,\"distinguished\":null,\"subreddit_id\":\"t5_2qh16\",\"author_is_blocked\":false,\"mod_reason_by\":null,\"num_reports\":null,\"removal_reason\":null,\"link_flair_background_color\":\"\",\"id\":\"1ocgytv\",\"is_robot_indexable\":true,\"report_reasons\":null,\"author\":\"ImCalcium\",\"discussion_type\":null,\"num_comments\":430,\"send_replies\":true,\"contest_mode\":false,\"mod_reports\":[],\"author_patreon_flair\":false,\"author_flair_text_color\":null,\"permalink\":\"/r/technology/comments/1ocgytv/aws_crash_causes_2000_smart_beds_to_overheat_and/\",\"stickied\":false,\"url\":\"https://www.dexerto.com/entertainment/aws-crash-causes-2000-smart-beds-to-overheat-and-get-stuck-upright-3272251/\",\"subreddit_subscribers\":19951849,\"created_utc\":1761062652,\"num_crossposts\":1,\"media\":null,\"is_video\":false}},{\"kind\":\"t3\",\"data\":{\"approved_at_utc\":null,\"subreddit\":\"technology\",\"selftext\":\"\",\"author_fullname\":\"t2_2uwit82z\",\"saved\":false,\"mod_reason_title\":null,\"gilded\":0,\"clicked\":false,\"title\":\"Disney+andHuluSubscriptionCancellationsDoubledAfterJimmyKimmelSuspension|Socialmediausershadcalledforaboycott.\",\"link_flair_richtext\":[],\"subreddit_name_prefixed\":\"r/technology\",\"hidden\":false,\"pwls\":6,\"link_flair_css_class\":\"general\",\"downs\":0,\"thumbnail_height\":78,\"top_awarded_type\":null,\"hide_score\":false,\"name\":\"t3_1oca33n\",\"quarantine\":false,\"link_flair_text_color\":\"dark\",\"upvote_ratio\":0.95,\"author_flair_background_color\":null,\"ups\":3852,\"total_awards_received\":0,\"media_embed\":{},\"thumbnail_width\":140,\"author_flair_template_id\":null,\"is_original_content\":false,\"user_reports\":[],\"secure_media\":null,\"is_reddit_media_domain\":false,\"is_meta\":false,\"category\":null,\"secure_media_embed\":{},\"link_flair_text\":\"Networking/Telecom\",\"can_mod_post\":false,\"score\":3852,\"approved_by\":null,\"is_created_from_ads_ui\":false,\"author_premium\":true,\"thumbnail\":\"https://external-preview.redd.it/h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8.jpeg?width=140&height=78&auto=webp&s=63ba48598a765fc9d3e184efbbfa92370a952a8c\",\"edited\":false,\"author_flair_css_class\":null,\"author_flair_richtext\":[],\"gildings\":{},\"post_hint\":\"link\",\"content_categories\":null,\"is_self\":false,\"subreddit_type\":\"public\",\"created\":1761045106,\"link_flair_type\":\"text\",\"wls\":6,\"removed_by_category\":null,\"banned_by\":null,\"author_flair_type\":\"text\",\"domain\":\"gizmodo.com\",\"allow_live_comments\":false,\"selftext_html\":null,\"likes\":null,\"suggested_sort\":null,\"banned_at_utc\":null,\"url_overridden_by_dest\":\"https://gizmodo.com/disney-and-hulu-subscription-cancellations-doubled-after-jimmy-kimmel-suspension-2000674405\",\"view_count\":null,\"archived\":false,\"no_follow\":false,\"is_crosspostable\":false,\"pinned\":false,\"over_18\":false,\"preview\":{\"images\":[{\"source\":{\"url\":\"https://external-preview.redd.it/h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8.jpeg?auto=webp&s=a954cd9e9697e7ea16f371d896154140440afc2b\",\"width\":1200,\"height\":675},\"resolutions\":[{\"url\":\"https://external-preview.redd.it/h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8.jpeg?width=108&crop=smart&auto=webp&s=58ac74463d479f84e5157681bfae5e631f7ee459\",\"width\":108,\"height\":60},{\"url\":\"https://external-preview.redd.it/h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8.jpeg?width=216&crop=smart&auto=webp&s=30f195780626e6487a8bb73891282dc62dc2fcc6\",\"width\":216,\"height\":121},{\"url\":\"https://external-preview.redd.it/h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8.jpeg?width=320&crop=smart&auto=webp&s=1e2da2fef0e223b2ebf859f399c5ee790ed93577\",\"width\":320,\"height\":180},{\"url\":\"https://external-preview.redd.it/h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8.jpeg?width=640&crop=smart&auto=webp&s=d7adeb0ade8ad6ca52b3020f10595f556c5dda63\",\"width\":640,\"height\":360},{\"url\":\"https://external-preview.redd.it/h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8.jpeg?width=960&crop=smart&auto=webp&s=41274622ac10d4a10371398bf739177997bed9a7\",\"width\":960,\"height\":540},{\"url\":\"https://external-preview.redd.it/h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8.jpeg?width=1080&crop=smart&auto=webp&s=7fd14c851c47deaa07002f291fafb54331991df3\",\"width\":1080,\"height\":607}],\"variants\":{},\"id\":\"h7nVyfvqA0jXYCzTT5wprujo-FfRgeJVJCRJuf750j8\"}],\"enabled\":false},\"all_awardings\":[],\"awarders\":[],\"media_only\":false,\"link_flair_template_id\":\"69c9e74a-a816-11e9-b15f-0efdc827626c\",\"can_gild\":false,\"spoiler\":false,\"locked\":false,\"author_flair_text\":null,\"treatment_tags\":[],\"visited\":false,\"removed_by\":null,\"mod_note\":null,\"distinguished\":null,\"subreddit_id\":\"t5_2qh16\",\"author_is_blocked\":false,\"mod_reason_by\":null,\"num_reports\":null,\"removal_reason\":null,\"link_flair_background_color\":\"\",\"id\":\"1oca33n\",\"is_robot_indexable\":true,\"report_reasons\":null,\"author\":\"chrisdh79\",\"discussion_type\":null,\"num_comments\":168,\"send_replies\":false,\"contest_mode\":false,\"mod_reports\":[],\"author_patreon_flair\":false,\"author_flair_text_color\":null,\"permalink\":\"/r/technology/comments/1oca33n/disney_and_hulu_subscription_cancellations/\",\"stickied\":false,\"url\":\"https://gizmodo.com/disney-and-hulu-subscription-cancellations-doubled-after-jimmy-kimmel-suspension-2000674405\",\"subreddit_subscribers\":19951849,\"created_utc\":1761045106,\"num_crossposts\":0,\"media\":null,\"is_video\":false}}]}}"
    response = json.loads(response)

    print(params)
    # response = reddit_client.make_request(SUBREDDIT_URL, params=params)
    posts = []

    if response:
        try:
            next_page = response["data"].get("after", None)
            children = response["data"].get("children", [])

            logger.debug(f"Next Page: {next_page}")

            for child in children:
                data = child["data"]

                # Log relevant community fields
                for field in POST_FIELDS:
                    logger.debug(f"{field}: {data.get(field, '')}")

                post_data_dict = {field: data.get(field, '') for field in POST_FIELDS}

                # Create community object using the dictionary
                post = Post(**post_data_dict)

                posts.append(post)

            return posts, next_page

        except (KeyError, TypeError, ValueError) as e:
            logger.error(f"Error parsing subreddit data: {e}")

    return [], None


def store_ps_in_db(posts: list):
    """
    Converts Communities list to tuples and inserts into the database.
    Uses bulk insert query via PLSQL helper.
    """
    plsql = PLSQL()
    unique_subreddit_in_db = plsql.get_data_from(SELECT_unique_name_QUERY)
    unique_subreddit_names = {row[0] for row in unique_subreddit_in_db}
    communities_data = [
        community.to_tuple()
        for community in posts
        if community.get_unique_name() not in unique_subreddit_names
    ]
    if (len(communities_data) == 0):
        logger.info("No New Communities Found")
    else:
        plsql.insert_bulk_data_into_db(BULK_INSERT_COMMUNITIES, communities_data)
        plsql.close_connection()


def get_posts():
    """
    Fetches data 4 times, waiting 15 seconds between requests,
    paginating through the results and storing each batch in DB.
    """
    logger.info("Starting SubReddit Posts fetch cycle")
    after = None
    finished = False

    while not finished:
        logger.info("Starting new 1-minute cycle with 4 requests")
        for i in range(4):
            logger.info(f"Fetching batch {i + 1}/4")
            posts, after = fetch_posts(after)
            if posts:
                store_ps_in_db(posts)
                logger.info(f"Stored batch {i + 1} with {len(posts)} posts")
            else:
                logger.warning(f"No data fetched on batch {i + 1}")

            if not after:
                logger.info("No more pages available, finished fetching all data")
                finished = True
                break

            if i < 3:  # Sleep only between requests, not after last one
                logger.info("Sleeping for 15 seconds before next request")
                time.sleep(15)

        if not finished:
            logger.info("Completed 4 requests this minute, waiting until next minute")
            # Sleep to complete the 60 second minute cycle,
            # subtracting time spent on 4 requests + sleeps
            # Each request + sleep ~15 seconds * 3 intervals = 45 seconds approx.
            # You can adjust this if needed.
            time.sleep(15)
            finished = True

    logger.info("Finished fetching all Reddit posts")


if __name__ == "__main__":
    get_posts()
    # init_faktory_client(
    #     role=FAKTORY_CONSUMER_ROLE,
    #     queue="enqueue-crawl-community",
    #     jobtype="enqueue_crawl_community",
    #     fn=get_subreddit,
    # )
    # logger.info("Started")
    # communities, after = fetch_subreddit_communities()
    # logger.info("collected data")
    # logger.info(f"collected data: {communities}")
    # logger.info(f"after: {after}")
    # store_communities_in_db(communities)
    # logger.info("Ended")
