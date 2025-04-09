#!/bin/bash
set -e

# Function to display usage information
show_usage() {
  echo "Morph Cloud Application"
  echo "======================="
  echo "Usage: docker-compose run morph-cloud-app [OPERATION]"
  echo ""
  echo "Operations:"
  echo "  create         - Create a new snapshot"
  echo "  list           - List all snapshots"
  echo "  get            - Get details of a specific snapshot (requires SNAPSHOT_ID env var)"
  echo "  delete         - Delete a specific snapshot (requires SNAPSHOT_ID env var)"
  echo "  create-instance - Create a new instance from a snapshot (requires SNAPSHOT_ID env var)"
  echo "  ssh            - SSH into a Morph Cloud instance (requires INSTANCE_ID env var)"
  echo "  all            - Run the comprehensive manager example"
  echo "  help           - Show this help message"
  echo ""
  echo "Environment Variables:"
  echo "  MORPH_API_KEY - Your Morph Cloud API key (required)"
  echo "  SNAPSHOT_ID   - ID of the snapshot for get/delete/create-instance operations"
  echo "  INSTANCE_ID   - ID of the instance for SSH operation"
  echo "  INSTANCE_NAME - Optional name for new instances (create-instance operation)"
  echo "  VCPUS         - Number of virtual CPUs for create operation (default: 2)"
  echo "  MEMORY        - Memory in MB for create operation (default: 4096)"
  echo "  DISK_SIZE     - Disk size in MB for create operation (default: 50000)"
  echo "  DIGEST        - Optional digest for create operation"
  echo ""
  echo "Examples:"
  echo "  docker-compose run -e SNAPSHOT_ID=abc123 morph-cloud-app get"
  echo "  docker-compose run -e VCPUS=4 -e MEMORY=8192 morph-cloud-app create"
  echo "  docker-compose run -e SNAPSHOT_ID=abc123 -e INSTANCE_NAME=my-server morph-cloud-app create-instance"
  echo "  docker-compose run -e INSTANCE_ID=inst123 morph-cloud-app ssh"
}

# Create data directory if it doesn't exist
mkdir -p /app/data

# Check if an operation is specified
OPERATION=${1:-help}

# Get environment variables with defaults
VCPUS=${VCPUS:-2}
MEMORY=${MEMORY:-4096}
DISK_SIZE=${DISK_SIZE:-50000}
DIGEST=${DIGEST:-}
INSTANCE_ID=${INSTANCE_ID:-}
INSTANCE_NAME=${INSTANCE_NAME:-}

# Log startup information
echo "$(date): Starting Morph Cloud application with operation: $OPERATION" | tee -a /app/data/app.log

# Execute the requested operation
case "$OPERATION" in
  create)
    echo "Creating a new snapshot with VCPUS=$VCPUS, MEMORY=$MEMORY, DISK_SIZE=$DISK_SIZE..."
    # Modify the create_snapshot.py file with the environment variables
    sed -i "s/vcpus=2/vcpus=$VCPUS/" /app/create_snapshot.py
    sed -i "s/memory=4096/memory=$MEMORY/" /app/create_snapshot.py
    sed -i "s/disk_size=50000/disk_size=$DISK_SIZE/" /app/create_snapshot.py
    
    if [ -n "$DIGEST" ]; then
      sed -i "s/digest=\"example-digest\"/digest=\"$DIGEST\"/" /app/create_snapshot.py
    fi
    
    python /app/create_snapshot.py | tee -a /app/data/app.log
    ;;
  list)
    echo "Listing all snapshots..."
    python /app/list_snapshots.py | tee -a /app/data/app.log
    ;;
  get)
    if [ -z "$SNAPSHOT_ID" ]; then
      echo "Error: SNAPSHOT_ID environment variable is required for this operation"
      show_usage
      exit 1
    fi
    echo "Getting details for snapshot $SNAPSHOT_ID..."
    # Replace the example ID with the provided one
    sed -i "s/snapshot_abc123/$SNAPSHOT_ID/" /app/get_snapshot_details.py
    python /app/get_snapshot_details.py | tee -a /app/data/app.log
    ;;
  delete)
    if [ -z "$SNAPSHOT_ID" ]; then
      echo "Error: SNAPSHOT_ID environment variable is required for this operation"
      show_usage
      exit 1
    fi
    echo "Deleting snapshot $SNAPSHOT_ID..."
    # Replace the example ID with the provided one
    sed -i "s/snapshot_abc123/$SNAPSHOT_ID/" /app/delete_snapshot.py
    python /app/delete_snapshot.py | tee -a /app/data/app.log
    ;;
  create-instance)
    if [ -z "$SNAPSHOT_ID" ]; then
      echo "Error: SNAPSHOT_ID environment variable is required for this operation"
      show_usage
      exit 1
    fi
    echo "Creating instance from snapshot $SNAPSHOT_ID..."
    if [ -n "$INSTANCE_NAME" ]; then
      echo "Using instance name: $INSTANCE_NAME"
    fi
    python /app/create_instance.py "$SNAPSHOT_ID" | tee -a /app/data/app.log
    ;;
  ssh)
    if [ -z "$INSTANCE_ID" ]; then
      echo "Error: INSTANCE_ID environment variable is required for this operation"
      show_usage
      exit 1
    fi
    echo "Connecting to instance $INSTANCE_ID via SSH..."
    python /app/ssh_to_instance.py "$INSTANCE_ID" | tee -a /app/data/app.log
    ;;
  all)
    echo "Running comprehensive manager example..."
    python /app/morph_cloud_manager.py | tee -a /app/data/app.log
    ;;
  help|--help|-h)
    show_usage
    ;;
  *)
    echo "Unknown operation: $OPERATION"
    show_usage
    exit 1
    ;;
esac

# Log completion
echo "$(date): Operation $OPERATION completed" | tee -a /app/data/app.log
