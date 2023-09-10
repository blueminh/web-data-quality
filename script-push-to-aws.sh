#!/bin/bash
frontendversion="2.6"
backendversion="2.7"

docker tag web-data-quality-backend:$backendversion minhkau/web-data-quality-backend:$backendversion
docker push minhkau/web-data-quality-backend:$backendversion

docker tag web-data-quality-frontend:$frontendversion minhkau/web-data-quality-frontend:$frontendversion
docker push minhkau/web-data-quality-frontend:$frontendversion
