import subprocess
import json

# Get the Azure AD Tenant ID
result = subprocess.run(['az', 'account', 'show', '--query', 'tenantId', '--output', 'json'], capture_output=True, text=True)
if result.returncode == 0:
    tenant_id = json.loads(result.stdout)
    tenant_id = tenant_id.strip('"')

    # Get all applications
    result = subprocess.run(['az', 'ad', 'app', 'list', '--all', '--query', "[].{displayName:displayName, appId:appId}", '--output', 'json'], capture_output=True, text=True)

    if result.returncode == 0:
        applications = json.loads(result.stdout)

        # Filter applications that start with 'AWS Console'
        filtered_apps = [app for app in applications if app['displayName'].startswith('AWS Console')]

        # Generate the configuration file content
        config_content = ""
        for app in filtered_apps:
            # Extract required information
            app_name = app['displayName']
            app_name_parts = app_name.split("-")  # Split the name by hyphen
            if len(app_name_parts) > 1:
                profile_name = app_name_parts[1].strip()  # Use the second part after hyphen
            else:
                profile_name = app_name.strip()  # Use the full name if no hyphen present
            profile_name = profile_name.replace(" ", "")  # Remove spaces from the profile name
            app_id = app['appId']

            # Replace <azure_tenant_id> with the Azure tenant value
            config_section = f"[profile {profile_name}]\n" \
                            f"azure_tenant_id={tenant_id}\n" \
                            f"azure_app_id_uri={app_id}\n" \
                            f"azure_default_username=<az_username>\n" \
                            f"azure_default_role_arn=<role_name>\n" \
                            f"azure_default_duration_hours=1\n" \
                            f"azure_default_remember_me=true\n\n"

            # Append the section to the config content
            config_content += config_section

        # Write the config content to a file
        with open("enterprise_config", "w") as config_file:
            config_file.write(config_content)

        print("Configuration file 'enterprise_config' generated successfully.")
    else:
        print("Error:", result.stderr)
else:
    print("Error:", result.stderr)
