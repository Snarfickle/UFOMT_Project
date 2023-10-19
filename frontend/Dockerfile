# Use the official Node.js LTS image as the base image
FROM node:lts-bullseye AS build

# Set the working directory
WORKDIR /app

# Copy package*.json files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Build the React application for production
RUN npm run build

# Use a Node.js image to run the production server
FROM node:lts-bullseye

# Set the working directory
WORKDIR /app

# Install the 'serve' package globally
RUN npm install -g serve

# Copy the build directory from the previous stage
COPY --from=build /app/build ./build

# Start the 'serve' server on port 80
CMD ["serve", "-s", "build", "-l", "80"]
