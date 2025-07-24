# Legal Knowledge Platform - Terraform Infrastructure

This Terraform configuration creates a production-ready VPC infrastructure for the Legal Knowledge Platform in your AWS Sandbox account.

## Architecture

- **VPC**: 10.1.0.0/16 with DNS hostnames enabled
- **Public Subnets**: 10.1.1.0/24, 10.1.2.0/24 (for ALB and NAT Gateways)
- **Private Subnets**: 10.1.10.0/24, 10.1.20.0/24 (for EC2 instances)
- **NAT Gateways**: High availability with one per AZ
- **Application Load Balancer**: Internet-facing for secure access
- **Security Groups**: Properly configured for ALB → EC2 communication
- **Key Pair**: For SSH access to instances

## Prerequisites

1. **Terraform installed** (>= 1.0)
   ```bash
   # macOS
   brew install terraform
   
   # Or download from https://terraform.io/downloads
   ```

2. **AWS CLI configured** for us-east-2 region
   ```bash
   aws configure list
   # Should show us-east-2 as default region
   ```

3. **SSH Key Pair**
   ```bash
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/legal-knowledge-platform
   # This creates ~/.ssh/legal-knowledge-platform and ~/.ssh/legal-knowledge-platform.pub
   ```

## Setup Steps

### 1. Add Your SSH Public Key

Copy your SSH public key content to `terraform/terraform.tfvars`:

```bash
# Get your public key content
cat ~/.ssh/legal-knowledge-platform.pub

# Edit terraform/terraform.tfvars and paste the key content
# public_key_content = "ssh-rsa AAAAB3NzaC1yc2EAAAA... your-email@example.com"
```

### 2. Initialize Terraform

```bash
cd /Users/johnfly/develop/firmpilot/dataLibrary/Production/terraform
terraform init
```

### 3. Plan (Check what will be created)

```bash
terraform plan
```

This shows you exactly what resources will be created. Review the output carefully.

### 4. Apply (Create the infrastructure)

```bash
terraform apply
```

Type `yes` when prompted. This takes about 5-10 minutes.

## What Gets Created

- 1 VPC with DNS support
- 4 subnets (2 public, 2 private) across 2 AZs
- 1 Internet Gateway
- 2 NAT Gateways with Elastic IPs
- 4 Route Tables (1 public, 2 private, 1 main)
- 1 Application Load Balancer
- 2 Security Groups (ALB and EC2)
- 1 Key Pair for SSH access

## Outputs

After successful apply, you'll see:
- VPC and subnet IDs
- Security group IDs
- ALB DNS name
- SSH command template
- EC2 launch command
- Cost estimates

## Next Steps

1. **Launch EC2 Instance**:
   ```bash
   # Use the command from terraform output
   terraform output -raw ec2_launch_command | bash
   ```

2. **Connect via SSH**:
   ```bash
   # First, get the instance private IP from AWS console
   ssh -i ~/.ssh/legal-knowledge-platform ubuntu@PRIVATE_IP
   ```

3. **Configure ALB Target Groups** (when ready to expose services)

## Cost Estimate

- **Monthly VPC Infrastructure**: ~$67
  - NAT Gateways (2): $45/month
  - Application Load Balancer: $17/month
  - Data Transfer: ~$5/month

- **EC2 Instance** (when launched):
  - g4dn.xlarge Spot: ~$144/month
  - g4dn.xlarge On-Demand: ~$360/month

## Managing Infrastructure

```bash
# Navigate to terraform directory
cd terraform

# See current state
terraform show

# See outputs
terraform output

# Modify and apply changes
terraform plan
terraform apply

# Destroy everything (when done)
terraform destroy
```

## Security Features

- EC2 instances in private subnets (no direct internet access)
- NAT Gateways for outbound internet access
- Security groups restrict access to your IP (107.197.112.114)
- ALB provides secure public access point
- Ready for Client VPN integration (172.31.0.0/16 CIDR pre-configured)

## Troubleshooting

**"Error: no matching EC2 Key Pair found"**
- Make sure you've added your public key content to `terraform.tfvars`

**"Error: UnauthorizedOperation"** 
- Check your AWS credentials and permissions

**"Error: availability zone not supported"**
- The configuration automatically uses available AZs in us-east-2

**Infrastructure already exists**
- Terraform is idempotent - it will only create what doesn't exist
- Use `terraform plan` to see what changes will be made