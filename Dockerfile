FROM nginx

# Copy the nginx configuration file into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports 80 and 443
EXPOSE 8000

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
