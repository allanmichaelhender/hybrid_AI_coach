# Use an official Node.js LTS runtime as a parent image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /app/frontend

# Copy package.json and the lock file
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application's code into the container
COPY . .

# Accept build argument for API URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the frontend for production
RUN npm run build

# Expose the default Vite port (optional, for debugging)
EXPOSE 5173

# Define the command to clear volume and copy files at runtime
CMD ["sh", "-c", "rm -rf /app/dist/* && cp -r /app/frontend/dist/* /app/dist/ && while true; do sleep 30; done"]
