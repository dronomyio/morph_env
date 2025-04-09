FROM python:3.10-slim

WORKDIR /app

# Install SSH client
RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY morph_cloud_manager.py .
COPY create_snapshot.py .
COPY list_snapshots.py .
COPY get_snapshot_details.py .
COPY delete_snapshot.py .
COPY ssh_to_instance.py .
COPY create_instance.py .
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Create .ssh directory for SSH keys
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

# Set environment variables if needed
# ENV MORPH_API_KEY=your_api_key_here

# Run the application
ENTRYPOINT ["/app/entrypoint.sh"]
