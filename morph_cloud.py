#!/usr/bin/env python3


# SSH into an instance (will offer to start it if not running)
#./morph_cloud.sh ssh --instance-id morphvm_oqv3oisg

from morphcloud.api import MorphCloudClient
import os
import sys
import time
import argparse

class MorphCloudManager:
    """
    A comprehensive manager for Morph Cloud operations.
    This class provides methods for all operations available in the Morph Cloud API.
    """
    
    def __init__(self, api_key=None):
        """Initialize the Morph Cloud client with API key"""
        # Get API key from parameter, environment variable, or config file
        self.api_key = api_key or os.environ.get('MORPH_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key must be provided or set in MORPH_API_KEY environment variable")
            
        # Initialize the client with API key
        self.client = MorphCloudClient(api_key=self.api_key)
    
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
        try:
            print(f"Creating snapshot with VCPUS={vcpus}, MEMORY={memory}, DISK_SIZE={disk_size}...")
            new_snapshot = self.client.snapshots.create(
                vcpus=vcpus,
                memory=memory,
                disk_size=disk_size,
                digest=digest
            )
            print(f"Snapshot created with ID: {new_snapshot.id}")
            return new_snapshot
        except Exception as e:
            print(f"Error creating snapshot: {str(e)}")
            return None
    
    def list_snapshots(self):
        """
        List all snapshots in your Morph Cloud account.
        
        Returns:
            List of snapshot objects
        """
        try:
            print("Listing all snapshots...")
            snapshots = self.client.snapshots.list()
            
            if not snapshots:
                print("No snapshots found.")
                return []
                
            print(f"Found {len(snapshots)} snapshots:")
            for snapshot in snapshots:
                print(f"ID: {snapshot.id}, Created At: {snapshot.created}")
            return snapshots
        except Exception as e:
            print(f"Error listing snapshots: {str(e)}")
            return []
    
    def get_snapshot_details(self, snapshot_id):
        """
        Get detailed information about a specific snapshot.
        
        Args:
            snapshot_id (str): ID of the snapshot to retrieve
            
        Returns:
            The snapshot object with details
        """
        try:
            print(f"Getting details for snapshot {snapshot_id}...")
            snapshot = self.client.snapshots.get(snapshot_id=snapshot_id)
            
            print(f"Snapshot ID: {snapshot.id}")
            print(f"Created At: {snapshot.created}")
            # Print additional details if available
            for attr in dir(snapshot):
                if not attr.startswith('_') and attr not in ['id', 'created']:
                    value = getattr(snapshot, attr)
                    if not callable(value):
                        print(f"{attr}: {value}")
                        
            return snapshot
        except Exception as e:
            print(f"Error getting snapshot details: {str(e)}")
            return None
    
    def delete_snapshot(self, snapshot_id):
        """
        Delete a snapshot when it's no longer needed.
        
        Args:
            snapshot_id (str): ID of the snapshot to delete
        """
        try:
            print(f"Deleting snapshot {snapshot_id}...")
            self.client.snapshots.delete(snapshot_id=snapshot_id)
            print(f"Snapshot {snapshot_id} has been deleted")
            return True
        except Exception as e:
            print(f"Error deleting snapshot: {str(e)}")
            return False
            
    def create_instance(self, snapshot_id, name=None):
        """
        Create a new instance from a snapshot.
        
        Args:
            snapshot_id (str): ID of the snapshot to use
            name (str, optional): Name for the new instance
        
        Returns:
            The created instance object
        """
        try:
            print(f"Creating instance from snapshot {snapshot_id}...")
            
            # Use the correct method: start() instead of create()
            instance = self.client.instances.start(snapshot_id=snapshot_id)
            
            # Set name if provided (may need to be done separately depending on API)
            if name and hasattr(instance, 'name'):
                instance.name = name
                print(f"Instance named: {name}")
            
            print(f"Instance started with ID: {instance.id}")
            print(f"Status: {instance.status}")
            
            # Wait for instance to be ready
            if instance.status != "running":
                print("Waiting for instance to start...")
                for _ in range(30):  # Wait up to 30 seconds
                    time.sleep(1)
                    instance = self.client.instances.get(instance_id=instance.id)
                    if instance.status == "running":
                        print("Instance is now running.")
                        break
                else:
                    print("Note: Instance creation initiated but not yet running.")
                    print("Check status later or start it manually if needed.")
            
            print(f"\nTo SSH into this instance, use:")
            print(f"python {sys.argv[0]} ssh --instance-id {instance.id}")
            
            return instance
        except Exception as e:
            print(f"Error creating instance: {str(e)}")
            return None
            
    def list_instances(self):
        """
        List all instances in your Morph Cloud account.
        
        Returns:
            List of instance objects
        """
        try:
            print("Listing all instances...")
            instances = self.client.instances.list()
            
            if not instances:
                print("No instances found.")
                return []
                
            print(f"Found {len(instances)} instances:")
            for instance in instances:
                print(f"ID: {instance.id}, Status: {instance.status}")
                if hasattr(instance, 'name') and instance.name:
                    print(f"  Name: {instance.name}")
                if hasattr(instance, 'refs') and hasattr(instance.refs, 'snapshot_id'):
                    print(f"  Snapshot ID: {instance.refs.snapshot_id}")
            return instances
        except Exception as e:
            print(f"Error listing instances: {str(e)}")
            return []
            
    def get_instance_details(self, instance_id):
        """
        Get detailed information about a specific instance.
        
        Args:
            instance_id (str): ID of the instance to retrieve
            
        Returns:
            The instance object with details
        """
        try:
            print(f"Getting details for instance {instance_id}...")
            instance = self.client.instances.get(instance_id=instance_id)
            
            print(f"Instance ID: {instance.id}")
            if hasattr(instance, 'name') and instance.name:
                print(f"Name: {instance.name}")
            print(f"Status: {instance.status}")
            
            # Print additional details if available
            for attr in dir(instance):
                if not attr.startswith('_') and attr not in ['id', 'name', 'status']:
                    value = getattr(instance, attr)
                    if not callable(value):
                        print(f"{attr}: {value}")
                        
            return instance
        except Exception as e:
            print(f"Error getting instance details: {str(e)}")
            return None
            
    def delete_instance(self, instance_id):
        """
        Delete an instance when it's no longer needed.
        
        Args:
            instance_id (str): ID of the instance to delete
        """
        try:
            print(f"Stopping instance {instance_id}...")
            instance = self.client.instances.get(instance_id=instance_id)
            instance.stop()
            print(f"Instance {instance_id} has been stopped")
            return True
        except Exception as e:
            print(f"Error stopping instance: {str(e)}")
            return False
            
    def start_instance(self, instance_id):
        """
        Start a stopped instance.
        
        Args:
            instance_id (str): ID of the instance to start
        """
        try:
            print(f"Starting instance {instance_id}...")
            
            # Get the instance details first
            instance = self.client.instances.get(instance_id=instance_id)
            
            if instance.status == "running":
                print("Instance is already running.")
                return instance
            
            # Get the snapshot ID associated with this instance
            snapshot_id = None
            if hasattr(instance, 'refs') and hasattr(instance.refs, 'snapshot_id'):
                snapshot_id = instance.refs.snapshot_id
            
            if not snapshot_id:
                print("Error: Could not determine the snapshot ID for this instance.")
                return None
            
            # Start a new instance using the same snapshot ID
            print(f"Starting instance using snapshot ID: {snapshot_id}")
            new_instance = self.client.instances.start(snapshot_id=snapshot_id)
            
            print(f"Instance started with ID: {new_instance.id}")
            print(f"Status: {new_instance.status}")
            
            # Wait for instance to be ready
            if new_instance.status != "running":
                print("Waiting for instance to start...")
                for _ in range(30):  # Wait up to 30 seconds
                    time.sleep(1)
                    new_instance = self.client.instances.get(instance_id=new_instance.id)
                    if new_instance.status == "running":
                        print("Instance is now running.")
                        break
                else:
                    print("Note: Instance start initiated but not yet running.")
                    print("Check status later.")
            
            return new_instance
        except Exception as e:
            print(f"Error starting instance: {str(e)}")
            return None
            
    def stop_instance(self, instance_id):
        """
        Stop a running instance.
        
        Args:
            instance_id (str): ID of the instance to stop
        """
        try:
            print(f"Stopping instance {instance_id}...")
            instance = self.client.instances.get(instance_id=instance_id)
            
            if instance.status != "running":
                print(f"Instance is not running (status: {instance.status}).")
                return instance
                
            instance.stop()
            print("Waiting for instance to stop...")
            
            # Wait for instance to stop
            for _ in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                instance = self.client.instances.get(instance_id=instance_id)
                if instance.status != "running":
                    print(f"Instance is now {instance.status}.")
                    break
            else:
                print("Note: Stop command sent but instance still running.")
                print("Check status later.")
                
            return instance
        except Exception as e:
            print(f"Error stopping instance: {str(e)}")
            return None
            
    def ssh_to_instance(self, instance_id):
        """
        SSH into a specific Morph Cloud instance.
        
        Args:
            instance_id (str): ID of the instance to SSH into
        """
        try:
            print(f"Retrieving instance {instance_id}...")
            instance = self.client.instances.get(instance_id=instance_id)
            
            # Check if instance is running
            if instance.status != "running":
                print(f"Instance {instance_id} is not running (status: {instance.status})")
                choice = input("Do you want to start the instance? (y/n): ")
                if choice.lower() == 'y':
                    print(f"Starting instance {instance_id}...")
                    
                    # Get the snapshot ID associated with this instance
                    snapshot_id = None
                    if hasattr(instance, 'refs') and hasattr(instance.refs, 'snapshot_id'):
                        snapshot_id = instance.refs.snapshot_id
                    
                    if not snapshot_id:
                        print("Error: Could not determine the snapshot ID for this instance.")
                        return
                    
                    # Start a new instance using the same snapshot ID
                    print(f"Starting instance using snapshot ID: {snapshot_id}")
                    new_instance = self.client.instances.start(snapshot_id=snapshot_id)
                    instance_id = new_instance.id
                    
                    print(f"New instance started with ID: {instance_id}")
                    print("Waiting for instance to start...")
                    
                    # Wait for instance to start
                    for _ in range(30):  # Wait up to 30 seconds
                        time.sleep(1)
                        instance = self.client.instances.get(instance_id=instance_id)
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


def main():
    parser = argparse.ArgumentParser(description='Morph Cloud Manager')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create snapshot command
    create_snapshot_parser = subparsers.add_parser('create-snapshot', help='Create a new snapshot')
    create_snapshot_parser.add_argument('--vcpus', type=int, default=2, help='Number of virtual CPUs')
    create_snapshot_parser.add_argument('--memory', type=int, default=4096, help='Memory in MB')
    create_snapshot_parser.add_argument('--disk-size', type=int, default=50000, help='Disk size in MB')
    create_snapshot_parser.add_argument('--digest', help='Optional digest identifier')
    
    # List snapshots command
    subparsers.add_parser('list-snapshots', help='List all snapshots')
    
    # Get snapshot details command
    get_snapshot_parser = subparsers.add_parser('get-snapshot', help='Get details of a specific snapshot')
    get_snapshot_parser.add_argument('--snapshot-id', required=True, help='ID of the snapshot')
    
    # Delete snapshot command
    delete_snapshot_parser = subparsers.add_parser('delete-snapshot', help='Delete a snapshot')
    delete_snapshot_parser.add_argument('--snapshot-id', required=True, help='ID of the snapshot to delete')
    
    # Create instance command
    create_instance_parser = subparsers.add_parser('create-instance', help='Create a new instance from a snapshot')
    create_instance_parser.add_argument('--snapshot-id', required=True, help='ID of the snapshot to use')
    create_instance_parser.add_argument('--name', help='Name for the new instance')
    
    # List instances command
    subparsers.add_parser('list-instances', help='List all instances')
    
    # Get instance details command
    get_instance_parser = subparsers.add_parser('get-instance', help='Get details of a specific instance')
    get_instance_parser.add_argument('--instance-id', required=True, help='ID of the instance')
    
    # Delete instance command
    delete_instance_parser = subparsers.add_parser('delete-instance', help='Delete an instance')
    delete_instance_parser.add_argument('--instance-id', required=True, help='ID of the instance to delete')
    
    # Start instance command
    start_instance_parser = subparsers.add_parser('start-instance', help='Start a stopped instance')
    start_instance_parser.add_argument('--instance-id', required=True, help='ID of the instance to start')
    
    # Stop instance command
    stop_instance_parser = subparsers.add_parser('stop-instance', help='Stop a running instance')
    stop_instance_parser.add_argument('--instance-id', required=True, help='ID of the instance to stop')
    
    # SSH to instance command
    ssh_parser = subparsers.add_parser('ssh', help='SSH into a Morph Cloud instance')
    ssh_parser.add_argument('--instance-id', required=True, help='ID of the instance to SSH into')
    
    # Global arguments
    parser.add_argument('--api-key', help='Morph Cloud API key (can also be set via MORPH_API_KEY environment variable)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Initialize the manager
        manager = MorphCloudManager(api_key=args.api_key)
        
        # Execute the requested command
        if args.command == 'create-snapshot':
            manager.create_snapshot(vcpus=args.vcpus, memory=args.memory, disk_size=args.disk_size, digest=args.digest)
        elif args.command == 'list-snapshots':
            manager.list_snapshots()
        elif args.command == 'get-snapshot':
            manager.get_snapshot_details(args.snapshot_id)
        elif args.command == 'delete-snapshot':
            manager.delete_snapshot(args.snapshot_id)
        elif args.command == 'create-instance':
            manager.create_instance(args.snapshot_id, args.name)
        elif args.command == 'list-instances':
            manager.list_instances()
        elif args.command == 'get-instance':
            manager.get_instance_details(args.instance_id)
        elif args.command == 'delete-instance':
            manager.delete_instance(args.instance_id)
        elif args.command == 'start-instance':
            manager.start_instance(args.instance_id)
        elif args.command == 'stop-instance':
            manager.stop_instance(args.instance_id)
        elif args.command == 'ssh':
            manager.ssh_to_instance(args.instance_id)
    
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Hint: Set your API key using the --api-key option or the MORPH_API_KEY environment variable")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()

