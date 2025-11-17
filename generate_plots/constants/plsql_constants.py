GET_CHAN_TOXICITY_QUERY = "SELECT board_name, titleorcomment, post_no, toxicity, severe_toxicity, identity_attack, insult, threat, profanity, sexually_explicit, flirtation, obscene, spam, unsubstantial FROM toxicity limit 100"

GET_REDDIT_TOXICITY_QUERY = "SELECT subreddit, titleorcomment, unique_name, toxicity, severe_toxicity, identity_attack, insult, threat, profanity, sexually_explicit, flirtation, obscene, spam, unsubstantial FROM toxicity limit 100"
