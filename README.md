docker run -d -it --name faktory -v faktory-data:/var/lib/faktory/db -e "FAKTORY_PASSWORD=password" -p 127.0.0.1:7419:7419 -p 127.0.0.1:7420:7420 contribsys/faktory /faktory -b :7419 -w :7420

sqlx migrate add -r --source .\4chan_crawler\migrations\ "trail"

SQL COMMANDS

1. List all database
   1.  \l or \list
2. Connect to database or use database
   - \c <database_name>
3. List all the tables
   - \dt
4. 

SQL
 delete migrations
    DELETE FROM _sqlx_migrations WHERE version = '20251019155449';


- Research Areas

   1. ws_board for 4chan, over18 attribute from boards tell whether that contains nudity... in generally where it safe to see in work space
      - What content in social media is safe to children less 18
      - 
   

   2. Do we have any specific data regarding India country


Task to-do
1. Logger writing files should not overwrite the existing data ✅
2. For Logger give log file each crawler so you track easily 
3. Write documentation for all the files 
4. Before submitting format all files 



|**Board Code**|**Board title**|**Board description**|
|--------------|---------------|---------------------|
|**/pol/**|Politically Incorrect|Politically Incorrect is 4chan's board for discussing and debating politics and current events.|
|**/int/**|International|International is 4chan's international board, for the exchange of foreign language and culture.|
|**/g/**|Technology|Technology is 4chan's imageboard for discussing computer hardware and software, programming, and general technology.|
|**/news/**|Current News|Current News; is 4chan's board for current news.|
|**/out/**|Outdoors|Outdoors is 4chan's imageboard for discussing survivalist skills and outdoor activities such as hiking.|
|**/sp/**|Sports|Sports; is 4chan's imageboard for sports discussion.|
|**/xs/**|Extreme Sports|Extreme Sports is 4chan's imageboard imageboard dedicated to the discussion of extreme sports.|


4Chan
   News
      pol
      int
      news
   Sport
      sport
      xs
      out
   technology
      g

Reddit_crawler
   news
      r/worldnews
      r/geopolitics
   Sport
      r/Outdoors
   technology
      r/technology
      r/MachineLearning
      r/deeplearning
      r/artificial
      r/AutoGPT


after
dist
subreddit
author_fullname
gilded- The number of times this post has been "gilded" (given an award). 0 means no awards.
title
hidden-Indicates if the post is hidden by the user. false means it's not hidden.
pwls-This is a filter used to restrict certain content for specific types of users (such as age-restricted content). A value of 6 indicates a certain level of restrictions.
downs-The number of downvotes this post has received. 0 means no downvotes.
top_awarded_type-Indicates if the post has received any top awards (like "gold"). null means it hasn't.
hide_score: This indicates whether the score (upvotes - downvotes) is hidden. true means the score is hidden for this post.
name-The unique ID of the post. This can be used to reference the post directly in Reddit's system.
quarantine:Indicates whether the post has been quarantined by Reddit (usually for content violations or suspected spam). false means it’s not quarantined.
upvote_ratio: The ratio of upvotes to total votes. A value of 0.98 means 98% of votes are upvotes.
ups:The number of upvotes the post has received.
thumbnail-The URL of the post's thumbnail image.
edited: Whether the post has been edited. It’s false, meaning it hasn’t been edited after posting.
created:The timestamp (in seconds since the Unix epoch) when the post was created.
over_18:Whether the post is marked as NSFW (Not Safe For Work). It’s false, meaning it’s safe for work.
is_original_content:Whether the post is original content created by the user. false means it links to external content.
url_overridden_by_dest:The final destination URL that the post links to. Here, it's the external Dexerto article.
num_comments:
total_awards_received:
top_awarded_type-Indicates if the post has received any top awards (like "gold"). null means it hasn't.
domain:The domain the post links to. In this case, the post links to an article on Dexerto.
num_reports:The number of times a post has been reported by Reddit users.
removal_reason: If the post has been removed by a moderator or the system, this field contains the reason for removal.
id:A unique identifier for the post
is_robot_indexable: This field determines whether the post is robot indexable, meaning whether it can be crawled and indexed by search engines or bots.
author: The Reddit username of the person who posted the content.
is_video:This indicates whether the post is a video or not.
subreddit": "technology",
