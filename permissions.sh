#!/bin/bash

# Array of directories to exclude
EXCLUDE_DIRS=("Cars" "Education" "Games" "Weather" "Sports")

# Function to check if an array contains a value
contains() {
    local e match="$1"
    shift
    for e; do [[ "$e" == "$match" ]] && return 0; done
    return 1
}

# Prepare CSV file
csv_file="../apppermissions.csv"
echo "AppName, Permissions" > "$csv_file"

# Iterate over directories in the current directory
for dir in */ ; do
    # Check if directory is in the exclude list
    if contains "${dir%/}" "${EXCLUDE_DIRS[@]}"; then
        continue
    fi

    # Find application names (assuming they end with '.app')
    app_name=$(find "$dir" -name '*.app' -exec basename {} \;)

    # Find all .plist files, extract NS keys, and filter them
    ns_keys=$(find "$dir" -name '*.plist' -print0 | xargs -0 grep -h -o '<key>NS.*</key>' | sed -e 's/<key>\(.*\)<\/key>/\1/' | sort | uniq)

    # Check if NS keys are found
    if [ -n "$ns_keys" ]; then
        # Format and append the result to the CSV file
        echo "\"$app_name\", \"${ns_keys//$'\n'/, }\"" >> "$csv_file"
    fi
done
