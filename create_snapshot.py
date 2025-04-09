#!/usr/bin/env python3

from morphcloud.api import MorphCloudClient
import os

def create_snapshot(vcpus=2, memory=4096, disk_size=50000, digest=None):
    """
    Create a new snapshot in Morph Cloud with specified resources.
    
    Args:
        vcpus (int): Number of virtual CPUs
        memory (int): Memory in MB
        disk_size (int): Disk size in MB
        digest (str, optional): Optional digest identifier
        
    Returns:
        The created snapshot object
    """
    # Get API key from environment variable
    api_key = os.environ.get('MORPH_API_KEY')
    
    # Initialize the Morph Cloud client with API key
    client = MorphCloudClient(api_key=api_key)
    
    # Create a new snapshot with specified parameters
    new_snapshot = client.snapshots.create(
        vcpus=vcpus,
        memory=memory,
        disk_size=disk_size,
        digest=digest
    )
    
    print(f"Snapshot created with ID: {new_snapshot.id}")
    return new_snapshot

if __name__ == "__main__":
    # Get values from environment variables or use defaults
    vcpus = int(os.environ.get('VCPUS', 2))
    memory = int(os.environ.get('MEMORY', 4096))
    disk_size = int(os.environ.get('DISK_SIZE', 50000))
    digest = os.environ.get('DIGEST')
    
    # Example usage
    snapshot = create_snapshot(
        vcpus=vcpus,
        memory=memory,
        disk_size=disk_size,
        digest=digest
    )
