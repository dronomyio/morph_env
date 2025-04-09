#!/usr/bin/env python3

from morphcloud.api import MorphCloudClient
import os

def list_snapshots():
    """
    List all snapshots in your Morph Cloud account.
    
    Returns:
        List of snapshot objects
    """
    # Get API key from environment variable or use provided value
    api_key = os.environ.get('MORPH_API_KEY')
    
    # Initialize the Morph Cloud client with API key
    client = MorphCloudClient(api_key=api_key)
    
    # Get all snapshots
    snapshots = client.snapshots.list()
    
    # Print snapshot information
    for snapshot in snapshots:
        print(f"ID: {snapshot.id}, Created At: {snapshot.created}")
    
    return snapshots

if __name__ == "__main__":
    # Example usage
    list_snapshots()
