#!/usr/bin/env python3

from morphcloud.api import MorphCloudClient
import os

def delete_snapshot(snapshot_id):
    """
    Delete a snapshot when it's no longer needed.
    
    Args:
        snapshot_id (str): ID of the snapshot to delete
    """
    # Get API key from environment variable
    api_key = os.environ.get('MORPH_API_KEY')
    
    # Initialize the Morph Cloud client with API key
    client = MorphCloudClient(api_key=api_key)
    
    # Delete the snapshot
    client.snapshots.delete(snapshot_id=snapshot_id)
    
    print(f"Snapshot {snapshot_id} has been deleted")

if __name__ == "__main__":
    # Get snapshot ID from environment variable
    snapshot_id = os.environ.get('SNAPSHOT_ID', "snapshot_abc123")
    
    # Example usage
    delete_snapshot(snapshot_id)
