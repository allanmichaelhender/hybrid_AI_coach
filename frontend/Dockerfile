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

# Expose the default Vite port
EXPOSE 5174

# Define the command to run your app's development server
# The --host flag is important to expose the server to the Docker network
CMD ["npm", "run", "dev", "--", "--host"]
