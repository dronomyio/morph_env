# Morph Cloud Manager

A comprehensive command-line tool for managing Morph Cloud snapshots and instances.

## Features

- Create, list, view, and delete snapshots
- Create, list, view, and delete instances
- Start and stop instances
- SSH into instances
- Comprehensive error handling and user guidance
- Simple command-line interface

## Prerequisites

- Python 3.6+
- Morph Cloud SDK (`pip install morphcloud`)
- Morph Cloud API key
- SSH key registered with Morph Cloud (for SSH functionality)

## Installation

1. Download the `morph_cloud.py` script
2. Make it executable: `chmod +x morph_cloud.py`
3. Set your API key as an environment variable:
   ```bash
   export MORPH_API_KEY=your_api_key_here
   ```

## Usage

### Snapshot Management

**Create a new snapshot:**
```bash
python morph_cloud.py create-snapshot --vcpus 2 --memory 4096 --disk-size 50000
```

**List all snapshots:**
```bash
python morph_cloud.py list-snapshots
```

**Get snapshot details:**
```bash
python morph_cloud.py get-snapshot --snapshot-id your_snapshot_id
```

**Delete a snapshot:**
```bash
python morph_cloud.py delete-snapshot --snapshot-id your_snapshot_id
```

### Instance Management

**Create a new instance from a snapshot:**
```bash
python morph_cloud.py create-instance --snapshot-id your_snapshot_id --name my-instance
```

**List all instances:**
```bash
python morph_cloud.py list-instances
```

**Get instance details:**
```bash
python morph_cloud.py get-instance --instance-id your_instance_id
```

**Start an instance:**
```bash
python morph_cloud.py start-instance --instance-id your_instance_id
```

**Stop an instance:**
```bash
python morph_cloud.py stop-instance --instance-id your_instance_id
```

**Delete an instance:**
```bash
python morph_cloud.py delete-instance --instance-id your_instance_id
```

**SSH into an instance:**
```bash
python morph_cloud.py ssh --instance-id your_instance_id
```

### API Key Options

You can provide your API key in three ways:

1. As an environment variable:
   ```bash
   export MORPH_API_KEY=your_api_key_here
   ```

2. As a command-line argument:
   ```bash
   python morph_cloud.py list-snapshots --api-key your_api_key_here
   ```

3. In the `morph_cloud.sh` shell script (see below)

## Shell Script

For even easier usage, you can use the included `morph_cloud.sh` shell script:

```bash
./morph_cloud.sh create-snapshot
./morph_cloud.sh list-instances
./morph_cloud.sh ssh --instance-id your_instance_id
```

## Troubleshooting

### API Key Issues

If you encounter API key errors:
- Make sure your API key is correctly set as an environment variable or passed as an argument
- Verify that your API key has the necessary permissions

### SSH Issues

If you encounter SSH connection issues:
- Verify your SSH key is registered with Morph Cloud
- Check that the instance ID is correct
- Ensure the instance is running
- Verify your API key has the necessary permissions

## Examples

**Complete workflow example:**

```bash
# Create a new snapshot
python morph_cloud.py create-snapshot --vcpus 4 --memory 8192 --disk-size 100000
# Note the snapshot ID from the output

# Create an instance from the snapshot
python morph_cloud.py create-instance --snapshot-id your_snapshot_id --name my-server
# Note the instance ID from the output

# SSH into the instance
python morph_cloud.py ssh --instance-id your_instance_id

# When done, stop the instance
python morph_cloud.py stop-instance --instance-id your_instance_id
```
