#!/usr/bin/env python3

from morphcloud.api import MorphCloudClient
import os
import sys
import time

def create_instance(snapshot_id, name=None):
    """
    Create a new instance from a snapshot.
    
    Args:
        snapshot_id (str): ID of the snapshot to use
        name (str, optional): Name for the new instance
    
    Returns:
        The created instance object
    """
    # Get API key from environment variable
    api_key = os.environ.get('MORPH_API_KEY')
    
    # Initialize the Morph Cloud client with API key
    client = MorphCloudClient(api_key=api_key)
    
    # Create instance name if not provided
    if not name:
        name = f"instance-from-{snapshot_id[:8]}"
    
    try:
        # Create a new instance from the snapshot
        print(f"Creating instance '{name}' from snapshot {snapshot_id}...")
        instance = client.instances.create(
            snapshot_id=snapshot_id,
            name=name
        )
        
        print(f"Instance created with ID: {instance.id}")
        print(f"Status: {instance.status}")
        
        # Wait for instance to be ready
        if instance.status != "running":
            print("Waiting for instance to start...")
            for _ in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                instance = client.instances.get(instance_id=instance.id)
                if instance.status == "running":
                    print("Instance is now running.")
                    break
            else:
                print("Note: Instance creation initiated but not yet running.")
                print("Check status later or start it manually if needed.")
        
        print(f"\nTo SSH into this instance, use:")
        print(f"docker-compose run -e INSTANCE_ID={instance.id} morph-cloud-app ssh")
        
        return instance
        
    except Exception as e:
        print(f"Error creating instance: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Verify the snapshot ID is correct")
        print("2. Check that your API key has the necessary permissions")
        print("3. Ensure you have sufficient quota for new instances")
        print("4. Verify the snapshot is in a valid state")
        return None

if __name__ == "__main__":
    # Get snapshot ID from command line or environment variable
    if len(sys.argv) > 1:
        snapshot_id = sys.argv[1]
    else:
        snapshot_id = os.environ.get('SNAPSHOT_ID')
    
    # Get instance name from environment variable
    name = os.environ.get('INSTANCE_NAME')
    
    if not snapshot_id:
        print("Error: Snapshot ID must be provided as argument or set in SNAPSHOT_ID environment variable")
        print("\nUsage:")
        print("  python create_instance.py <snapshot_id> [instance_name]")
        print("  # OR")
        print("  export SNAPSHOT_ID=your_snapshot_id")
        print("  export INSTANCE_NAME=your_instance_name  # Optional")
        print("  python create_instance.py")
        sys.exit(1)
    
    # Create instance from snapshot
    create_instance(snapshot_id, name)
