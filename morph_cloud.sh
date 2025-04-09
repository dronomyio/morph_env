#!/bin/bash

# Morph Cloud Manager Shell Script
# A simple wrapper for the morph_cloud.py Python script

# Configuration
# Set your API key here or use environment variable
API_KEY=${MORPH_API_KEY:-""}

# Check if Python script exists
if [ ! -f "morph_cloud.py" ]; then
    echo "Error: morph_cloud.py not found in the current directory"
    echo "Please make sure the Python script is in the same directory as this shell script"
    exit 1
fi

# Make sure the Python script is executable
chmod +x morph_cloud.py

# Function to display usage information
show_usage() {
    echo "Morph Cloud Manager"
    echo "==================="
    echo "Usage: ./morph_cloud.sh COMMAND [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  create-snapshot   Create a new snapshot"
    echo "  list-snapshots    List all snapshots"
    echo "  get-snapshot      Get details of a specific snapshot"
    echo "  delete-snapshot   Delete a snapshot"
    echo "  create-instance   Create a new instance from a snapshot"
    echo "  list-instances    List all instances"
    echo "  get-instance      Get details of a specific instance"
    echo "  start-instance    Start a stopped instance"
    echo "  stop-instance     Stop a running instance"
    echo "  delete-instance   Delete an instance"
    echo "  ssh               SSH into a Morph Cloud instance"
    echo "  help              Show this help message"
    echo ""
    echo "For command-specific options, run:"
    echo "  ./morph_cloud.sh COMMAND --help"
    echo ""
    echo "Examples:"
    echo "  ./morph_cloud.sh create-snapshot --vcpus 4 --memory 8192"
    echo "  ./morph_cloud.sh list-snapshots"
    echo "  ./morph_cloud.sh create-instance --snapshot-id snap123 --name my-server"
    echo "  ./morph_cloud.sh ssh --instance-id inst123"
}

# Check if a command is provided
if [ $# -eq 0 ] || [ "$1" == "help" ] || [ "$1" == "--help" ]; then
    show_usage
    exit 0
fi

# Prepare the command
COMMAND="$1"
shift

# Execute the Python script with the provided command and arguments
# If API key is set, pass it as an environment variable
if [ -n "$API_KEY" ]; then
    MORPH_API_KEY="$API_KEY" python3 ./morph_cloud.py "$COMMAND" "$@"
else
    python3 ./morph_cloud.py "$COMMAND" "$@"
fi

