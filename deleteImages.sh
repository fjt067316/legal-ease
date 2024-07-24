#!/bin/bash

# Stop and remove all containers
docker-compose down

# Remove all Docker images associated with the project
# You may want to specify a more targeted filter if you only want to remove specific images
docker images -a | grep "legal-ease" | awk '{print $3}' | xargs docker rmi -f

# Optionally, remove all stopped containers and dangling images
docker container prune -f
docker image prune -f

echo "Containers stopped and removed, images deleted."