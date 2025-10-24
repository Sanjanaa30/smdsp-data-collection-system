if we are collecting specific boards data , should we hard code specific board name if not what should be do?
**Exposing Port for timescale-db**
- sudo docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password -v timescaledb-data:/var/lib/postgresql/data timescale/timescaledb-ha:pg17

**Installing Rust**
- curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
- source $HOME/.cargo/env
- rustc --version
- cargo --version


**Installing sqlx**
- cargo install sqlx-cli --no-default-features --features postgres
- sqlx --version

**Adding .env**
- SET DATABASE_URL={} 

**Creating Database**
- sqlx database create
- sqlx migrate run


Social Media

**Activating Venv**
- source .venv/bin/activate

**DOCKER**
1. Status of Docker
    - systemctl status docker
2. List all Docker Containers running
    - docker ps
3. Stop the Docker
    - docker stop <container_id>
4. Removed the container
    - docker rm <container_id>
5. Docker restart
    - docker restart timescaledb

**Linux**
1. Faktory is listed and 7419 and 7420 are bound to 0.0.0.0
    - sudo ss -tuln | grep 7420

**Creating new User**
- sudo adduser <user_name>
- SMDSP@bing123

**Switching User**
- sudo su - <user_name>

**make user sudoers**
sudo usermod -aG sudo <user_name>

**Download Log File**
- sudo cp logs/reddit_crawler.log "../../../"
- scp <user_name>@<ip_address>:/home/reddit_crawler.log C:\Users\karth\Downloads\

**Activating .venv**
- source .venv/bin/activate