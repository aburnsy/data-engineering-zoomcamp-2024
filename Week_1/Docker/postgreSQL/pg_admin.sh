
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="andrewburns89@gmail.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pg-admin \
    dpage/pgadmin4:latest