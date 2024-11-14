#!/bin/bash

# Prompt the user to enter Azure AD Username
read -p "Enter Azure AD Username: " az_username

# Prompt the user to enter AWS Session Role Name
read -p "Enter AWS Session Role Name: " role_name

# Read the contents of the enterprise_config file
updated_config_content=$(cat enterprise_config)

# Replace the placeholders with user input values
updated_config_content="${updated_config_content//<az_username>/$az_username}"
updated_config_content="${updated_config_content//<role_name>/$role_name}"

# Description
static_content="
# This file was generated! Do not edit directly!
# timestamp=$(date +"%Y-%m-%d %H:%M:%S")

"

# Define the start and end markers
start_marker="#Start CDP One config"
end_marker="#End CDP One config"

# Append the updated configuration to the ~/.aws/config file
config_path=~/.aws/config

# Check if the file exists
if [ -f "$config_path" ]; then
    # Find the positions of the start and end markers
    start_pos=$(grep -n "$start_marker" "$config_path" | cut -d ':' -f 1)
    end_pos=$(grep -n "$end_marker" "$config_path" | cut -d ':' -f 1)

    # Remove the content between the start and end markers
    if [[ -n "$start_pos" && -n "$end_pos" ]]; then
        sed -i.bak "$start_pos,$end_pos d" "$config_path"
    elif [[ -n "$start_pos" ]]; then
        sed -i.bak "$start_pos,$ d" "$config_path"
    fi

    # Write the updated content with markers and static content
    echo -e "$start_marker\n$static_content$updated_config_content\n$end_marker" >> "$config_path"
else
    echo -e "$start_marker\n$static_content$updated_config_content\n$end_marker" >> "$config_path"
fi

echo "Updated configuration merged into ~/.aws/config successfully."
