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
    DELETE FROM _sqlx_migrations WHERE version = '20251013212255';


- Research Areas

   1. ws_board for 4chan, over18 attribute from boards tell whether that contains nudity... in generally where it safe to see in work space
      - What content in social media is safe to children less 18
      - 
   

   2. Do we have any specific data regarding India country


Task to-do
1. Logger writing files should not overwrite the existing data