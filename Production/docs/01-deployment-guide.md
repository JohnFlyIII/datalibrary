# Legal Knowledge Platform - AWS Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the Superlinked-based Legal Knowledge Platform on AWS using Amazon Linux 2023 with GPU support.

## Prerequisites

### AWS Infrastructure (Already Deployed)
- EC2 g4dn.xlarge instance with Tesla T4 GPU
- Amazon Linux 2023 with Deep Learning AMI
- Security groups configured for ports 8080 (Superlinked) and 6333 (Qdrant)
- VPC with proper networking setup

### Local Requirements
- SSH access to EC2 instance
- Docker and Docker Compose installed on EC2
- Python 3.9+ for preprocessing scripts

## Deployment Steps

### 1. Connect to EC2 Instance

```bash
# Connect via SSH (replace with your instance details)
ssh -i your-key.pem ec2-user@your-instance-ip

# Verify GPU access
nvidia-smi
```

### 2. Clone Repository and Setup Directory Structure

```bash
# Create project directory
mkdir -p /home/ec2-user/legal-platform
cd /home/ec2-user/legal-platform

# Create required directories
mkdir -p data/qdrant
mkdir -p logs
mkdir -p backups
```

### 3. Copy Application Files

Copy the following files to your EC2 instance:

```bash
# From your local machine
scp -i your-key.pem -r Production/superlinked-app/* ec2-user@your-instance-ip:/home/ec2-user/legal-platform/
```

Required files:
- `app.py` - Main application
- `schema/` - Schema definitions
- `spaces/` - All space configurations
- `docker-compose.yml` - Service configuration
- `Dockerfile` - Superlinked container build

### 4. Create Docker Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: legal-qdrant
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__LOG_LEVEL=INFO
      - QDRANT__STORAGE__STORAGE_PATH=/qdrant/storage
      - QDRANT__STORAGE__WAL__WAL_CAPACITY_MB=2048
      - QDRANT__STORAGE__OPTIMIZERS__MEMMAP_THRESHOLD=100000
    volumes:
      - ./data/qdrant:/qdrant/storage
    ports:
      - "6333:6333"
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G

  superlinked:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: legal-superlinked
    environment:
      - QDRANT_URL=http://qdrant:6333
      - SERVER_HOST=0.0.0.0
      - SERVER_PORT=8080
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
      - CUDA_VISIBLE_DEVICES=0
      - PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
    depends_on:
      - qdrant
    ports:
      - "8080:8080"
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### 5. Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 6. Create Requirements File

Create `requirements.txt`:

```txt
superlinked==0.1.0
sentence-transformers==2.2.2
torch==2.0.1
qdrant-client==1.7.0
uvicorn==0.24.0
fastapi==0.104.0
pydantic==2.4.0
numpy==1.24.3
pandas==2.0.3
```

### 7. Build and Start Services

```bash
# Build the Superlinked image
docker compose build

# Start all services
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f
```

### 8. Verify Deployment

```bash
# Check Qdrant health
curl http://localhost:6333/health

# Check Superlinked health
curl http://localhost:8080/health

# Test GPU utilization
nvidia-smi
```

### 9. Initialize Qdrant Collection

```bash
# Create the legal_knowledge collection
curl -X PUT http://localhost:6333/collections/legal_knowledge \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 768,
      "distance": "Cosine"
    },
    "optimizers_config": {
      "default_segment_number": 4,
      "memmap_threshold": 20000
    }
  }'
```

## Production Configuration

### 1. Performance Optimization

Edit the Docker Compose file for production workloads:

```yaml
# Add to superlinked service
environment:
  - OMP_NUM_THREADS=4
  - MKL_NUM_THREADS=4
  - TOKENIZERS_PARALLELISM=false
  - BATCH_SIZE=32  # Adjust based on GPU memory
  - MAX_WORKERS=4
```

### 2. Monitoring Setup

Create a monitoring script `monitor.sh`:

```bash
#!/bin/bash
# GPU utilization
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv

# Container stats
docker stats --no-stream

# Disk usage
df -h /home/ec2-user/legal-platform/data

# Service health
curl -s http://localhost:6333/health
curl -s http://localhost:8080/health
```

### 3. Backup Configuration

Create automated backup script `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/home/ec2-user/legal-platform/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup Qdrant data
docker exec legal-qdrant qdrant snapshot create legal_knowledge
docker cp legal-qdrant:/qdrant/storage/snapshots $BACKUP_DIR/qdrant_$TIMESTAMP

# Compress backup
tar -czf $BACKUP_DIR/backup_$TIMESTAMP.tar.gz $BACKUP_DIR/qdrant_$TIMESTAMP

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR/backup_$TIMESTAMP.tar.gz s3://your-backup-bucket/

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
```

### 4. Systemd Service

Create `/etc/systemd/system/legal-platform.service`:

```ini
[Unit]
Description=Legal Knowledge Platform
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ec2-user/legal-platform
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl enable legal-platform
sudo systemctl start legal-platform
```

## Ingestion Setup

### 1. Install Preprocessing Dependencies

```bash
# On EC2 instance
pip3 install --user \
  pypdf2 \
  openai \
  anthropic \
  tqdm \
  requests
```

### 2. Configure Preprocessing

Create `preprocess_config.py`:

```python
# API Configuration
OPENAI_API_KEY = "your-key"
ANTHROPIC_API_KEY = "your-key"

# Preprocessing settings
FACT_EXTRACTION_MODEL = "gpt-4"
SUMMARY_MODEL = "claude-3-sonnet"
BATCH_SIZE = 10
RATE_LIMIT_DELAY = 1.0

# Superlinked API
SUPERLINKED_URL = "http://localhost:8080"
```

### 3. Test Ingestion

```bash
# Test with a single document
python3 ingest_document.py --file sample.pdf --test

# Run full ingestion
python3 ingest_batch.py --directory /path/to/documents
```

## Troubleshooting

### Common Issues

1. **GPU Not Detected**
   ```bash
   # Check NVIDIA driver
   nvidia-smi
   
   # Restart Docker daemon
   sudo systemctl restart docker
   ```

2. **Out of Memory**
   ```bash
   # Reduce batch size in environment
   docker compose down
   # Edit docker-compose.yml BATCH_SIZE
   docker compose up -d
   ```

3. **Qdrant Connection Failed**
   ```bash
   # Check Qdrant logs
   docker logs legal-qdrant
   
   # Verify network
   docker network ls
   docker network inspect legal-platform_default
   ```

### Performance Tuning

1. **GPU Memory Management**
   - Monitor with `nvidia-smi -l 1`
   - Adjust `PYTORCH_CUDA_ALLOC_CONF` in docker-compose.yml
   - Reduce batch size if OOM errors occur

2. **Qdrant Optimization**
   - Increase `memmap_threshold` for large collections
   - Adjust `wal_capacity_mb` based on ingestion rate
   - Use multiple segments for better parallelization

3. **Network Optimization**
   - Use placement groups for multi-instance setup
   - Enable SR-IOV for enhanced networking
   - Configure VPC endpoints for S3 access

## Maintenance

### Daily Tasks
- Monitor GPU utilization and temperature
- Check disk space for Qdrant storage
- Review error logs
- Verify backup completion

### Weekly Tasks
- Update embeddings for modified documents
- Optimize Qdrant indices
- Review search performance metrics
- Test disaster recovery procedure

### Monthly Tasks
- Update Superlinked and dependencies
- Review and optimize query patterns
- Analyze usage patterns
- Plan capacity scaling

## Scaling Considerations

### Vertical Scaling
- Upgrade to g4dn.2xlarge for more GPU memory
- Increase EBS volume size as needed
- Add more system RAM for larger batches

### Horizontal Scaling
- Deploy multiple Superlinked instances behind ALB
- Use Qdrant cluster mode for distributed search
- Implement Redis for caching frequently accessed embeddings
- Consider auto-scaling groups for variable load

## Security Best Practices

1. **Network Security**
   - Keep services in private subnet
   - Use ALB for public access
   - Enable VPC Flow Logs
   - Configure WAF rules

2. **Access Control**
   - Use IAM roles for EC2
   - Implement API keys for Superlinked
   - Enable Qdrant authentication
   - Rotate credentials regularly

3. **Data Protection**
   - Encrypt EBS volumes
   - Use S3 encryption for backups
   - Enable CloudTrail logging
   - Implement data retention policies

## Support and Resources

- Superlinked Documentation: https://docs.superlinked.com
- Qdrant Documentation: https://qdrant.tech/documentation
- AWS Support: Via AWS Console
- Internal Team: legal-platform@company.com

## Next Steps

1. Complete initial document ingestion
2. Configure monitoring dashboards
3. Set up alerting rules
4. Train team on query patterns
5. Plan first production workload

---

*Last Updated: 2024*
*Version: 1.0*