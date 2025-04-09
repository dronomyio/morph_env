#!/usr/bin/env python3

from morphcloud.api import MorphCloudClient
import os
import sys
import time

def ssh_to_instance(instance_id):
    """
    SSH into a specific Morph Cloud instance.
    
    Args:
        instance_id (str): ID of the instance to SSH into
    """
    # Get API key from environment variable
    api_key = os.environ.get('MORPH_API_KEY')
    
    # Initialize the Morph Cloud client with API key
    client = MorphCloudClient(api_key=api_key)
    
    try:
        # Get the instance
        print(f"Retrieving instance {instance_id}...")
        instance = client.instances.get(instance_id=instance_id)
        
        # Check if instance is running
        if instance.status != "running":
            print(f"Instance {instance_id} is not running (status: {instance.status})")
            choice = input("Do you want to start the instance? (y/n): ")
            if choice.lower() == 'y':
                print(f"Starting instance {instance_id}...")
                instance.start()
                print("Waiting for instance to start...")
                # Wait for instance to start
                for _ in range(30):  # Wait up to 30 seconds
                    time.sleep(1)
                    instance = client.instances.get(instance_id=instance_id)
                    if instance.status == "running":
                        print("Instance is now running.")
                        break
                else:
                    print("Timed out waiting for instance to start.")
                    return
            else:
                print("SSH connection aborted.")
                return
        
        # Connect via SSH
        print(f"Connecting to instance {instance_id} via SSH...")
        instance.ssh()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your SSH key is registered with Morph Cloud")
        print("2. Verify the instance ID is correct")
        print("3. Check that your API key has the necessary permissions")
        print("4. Ensure the instance is accessible from your network")

if __name__ == "__main__":
    # Get instance ID from command line or environment variable
    if len(sys.argv) > 1:
        instance_id = sys.argv[1]
    else:
        instance_id = os.environ.get('INSTANCE_ID')
    
    if not instance_id:
        print("Error: Instance ID must be provided as argument or set in INSTANCE_ID environment variable")
        print("\nUsage:")
        print("  python ssh_to_instance.py <instance_id>")
        print("  # OR")
        print("  export INSTANCE_ID=your_instance_id")
        print("  python ssh_to_instance.py")
        sys.exit(1)
        
    # SSH to the instance
    ssh_to_instance(instance_id)
