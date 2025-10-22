if we are collecting specific boards data , should we hard code specific board name if not what should be do?

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

**Linux**
1. Faktory is listed and 7419 and 7420 are bound to 0.0.0.0
    - sudo ss -tuln | grep 7420