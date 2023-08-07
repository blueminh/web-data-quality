# ==== CONFIGURE =====
# Use a Node 16 base image
FROM node:16-alpine 
# Set the working directory to /app inside the container
WORKDIR /app
# Copy app files
COPY . .
# ==== BUILD =====
# Build the app
RUN npm install
# ==== RUN =======
EXPOSE 3000
# Start the app
CMD [ "npm", "start"]