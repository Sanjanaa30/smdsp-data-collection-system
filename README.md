docker run -d -it --name faktory -v faktory-data:/var/lib/faktory/db -e "FAKTORY_PASSWORD=password" -p 127.0.0.1:7419:7419 -p 127.0.0.1:7420:7420 contribsys/faktory /faktory -b :7419 -w :7420

sqlx migrate add -r --source .\4chan_crawler\migrations\ "trail"