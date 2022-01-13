import praw
from prawcore.exceptions import RequestException, ServerError
import re
from alertzy import Alertzy
from absl import logging, app
import os
from retry import retry
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_list('regions', ["us", "usa"], "Which region to filter down to")


@retry((RequestException, ServerError), tries=-1, delay=180, backoff=2, max_delay=60 * 20)
def run_monitor(alertzy,
                regions=None,
                apollo_app=False):
    """Monitors subreddit for new selling posts for selected region"""
    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        user_agent=os.getenv('USER_AGENT'),
        ratelimit_seconds=os.getenv('RATELIMIT_SECONDS')
    )

    subreddit = reddit.subreddit(os.getenv('SUBREDDIT_NAME'))
    logging.info(f'Start listening to stream for subreddit: {subreddit}')
    for submission in subreddit.stream.submissions(skip_existing=True):
        title = str.lower(submission.title)
        title_split = re.split(r'[.\[\]]+', title)
        in_region = any([r for r in regions if str.lower(r) in title_split])
        logging.debug(f"{title_split}:: {in_region}, {'selling' in title_split}")
        if "selling" in title_split and in_region:
            submission_url = submission.url.replace("https://", "apollo://") if apollo_app else submission.url
            submission_title_trimmed = re.sub("\[.*?]", "", submission.title).strip(),  # Remove Text in Brackets
            logging.info(f"New Selling posting: {''.join(submission_title_trimmed)}")

            alertzy.send_notification(None,
                                      title=submission_title_trimmed,
                                      url=submission_url,
                                      image_url=None)


def main(_):
    logging.set_verbosity(logging.INFO)
    alertzy = Alertzy(service_name=f"Reddit Monitor: {os.getenv('SUBREDDIT_NAME')}")

    run_monitor(regions=FLAGS.regions,
                alertzy=alertzy,
                apollo_app=True)


if __name__ == '__main__':
    app.run(main)
