#!/bin/bash

# This script is used to reload the systemd services
# It will stop the current services and start them again with the new configuration
# Usage: ./reload.sh

# Get the service list from the files in the current directory
service_list=$(ls ./*.service)
# Loop through each service file
for service in $service_list; do
    # Get the service name without the path
    service_name=$(basename "$service")
    # Copy the service file to the systemd directory
    cp "$service_name" /etc/systemd/system/
    # Stop the service
    systemctl stop "$service_name"
    # Reload the systemd manager configuration
    systemctl daemon-reload
    # Start the service again
    systemctl start "$service_name"
done
