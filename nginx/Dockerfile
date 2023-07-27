# Use the Nginx image
FROM nginx:1.17.1-alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own configuration
COPY nginx.conf /etc/nginx/conf.d/
