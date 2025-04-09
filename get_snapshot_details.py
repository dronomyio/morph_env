#!/usr/bin/env python3

from morphcloud.api import MorphCloudClient
import os

def get_snapshot_details(snapshot_id):
    """
    Get detailed information about a specific snapshot.
    
    Args:
        snapshot_id (str): ID of the snapshot to retrieve
        
    Returns:
        The snapshot object with details
    """
    # Get API key from environment variable
    api_key = os.environ.get('MORPH_API_KEY')
    
    # Initialize the Morph Cloud client with API key
    client = MorphCloudClient(api_key=api_key)
    
    # Get snapshot details
    snapshot = client.snapshots.get(snapshot_id=snapshot_id)
    
    # Print snapshot information
    print(f"Snapshot ID: {snapshot.id}")
    print(f"Created At: {snapshot.created}")
    
    return snapshot

if __name__ == "__main__":
    # Get snapshot ID from environment variable
    snapshot_id = os.environ.get('SNAPSHOT_ID', "snapshot_abc123")
    
    # Example usage
    get_snapshot_details(snapshot_id)
