#!/bin/bash
frontendversion="3.0.1"
backendversion="3.0.1"

docker tag web-data-quality-backend:$backendversion minhkau/web-data-quality-backend:$backendversion
docker push minhkau/web-data-quality-backend:$backendversion

docker tag web-data-quality-frontend:$frontendversion minhkau/web-data-quality-frontend:$frontendversion
docker push minhkau/web-data-quality-frontend:$frontendversion
