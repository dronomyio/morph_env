#!/usr/bin/env python3

from morphcloud.api import MorphCloudClient
import os

class MorphCloudManager:
    """
    A comprehensive manager for Morph Cloud snapshot operations.
    This class provides methods for all snapshot operations available in the Morph Cloud API.
    """
    
    def __init__(self):
        """Initialize the Morph Cloud client with API key from environment variable"""
        # Get API key from environment variable
        api_key = os.environ.get('MORPH_API_KEY')
        
        # Initialize the client with API key
        self.client = MorphCloudClient(api_key=api_key)
    
    def create_snapshot(self, vcpus=2, memory=4096, disk_size=50000, digest=None):
        """
        Create a new snapshot with specified resources.
        
        Args:
            vcpus (int): Number of virtual CPUs
            memory (int): Memory in MB
            disk_size (int): Disk size in MB
            digest (str, optional): Optional digest identifier
            
        Returns:
            The created snapshot object
        """
        new_snapshot = self.client.snapshots.create(
            vcpus=vcpus,
            memory=memory,
            disk_size=disk_size,
            digest=digest
        )
        print(f"Snapshot created with ID: {new_snapshot.id}")
        return new_snapshot
    
    def list_snapshots(self):
        """
        List all snapshots in your Morph Cloud account.
        
        Returns:
            List of snapshot objects
        """
        snapshots = self.client.snapshots.list()
        for snapshot in snapshots:
            print(f"ID: {snapshot.id}, Created At: {snapshot.created}")
        return snapshots
    
    def get_snapshot_details(self, snapshot_id):
        """
        Get detailed information about a specific snapshot.
        
        Args:
            snapshot_id (str): ID of the snapshot to retrieve
            
        Returns:
            The snapshot object with details
        """
        snapshot = self.client.snapshots.get(snapshot_id=snapshot_id)
        print(f"Snapshot ID: {snapshot.id}")
        print(f"Created At: {snapshot.created}")
        return snapshot
    
    def delete_snapshot(self, snapshot_id):
        """
        Delete a snapshot when it's no longer needed.
        
        Args:
            snapshot_id (str): ID of the snapshot to delete
        """
        self.client.snapshots.delete(snapshot_id=snapshot_id)
        print(f"Snapshot {snapshot_id} has been deleted")

# Example usage
if __name__ == "__main__":
    manager = MorphCloudManager()
    
    # Get values from environment variables or use defaults
    vcpus = int(os.environ.get('VCPUS', 2))
    memory = int(os.environ.get('MEMORY', 4096))
    disk_size = int(os.environ.get('DISK_SIZE', 50000))
    digest = os.environ.get('DIGEST')
    snapshot_id = os.environ.get('SNAPSHOT_ID')
    
    # Create a new snapshot
    new_snapshot = manager.create_snapshot(
        vcpus=vcpus,
        memory=memory,
        disk_size=disk_size,
        digest=digest
    )
    
    # List all snapshots
    all_snapshots = manager.list_snapshots()
    
    # Get details of a specific snapshot
    if snapshot_id:
        snapshot_details = manager.get_snapshot_details(snapshot_id)
    elif all_snapshots:
        snapshot_details = manager.get_snapshot_details(all_snapshots[0].id)
    
    # Delete a snapshot (uncomment to use)
    # if snapshot_id:
    #     manager.delete_snapshot(snapshot_id)
